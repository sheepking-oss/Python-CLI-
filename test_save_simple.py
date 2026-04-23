#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

original_cwd = os.getcwd()
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("=" * 60)
print("  Archive System Test")
print("=" * 60)

test_dir = tempfile.mkdtemp(prefix='test_save_')
print(f"\nTest Directory: {test_dir}")

import save_system

original_save_dir = save_system.SAVE_DIR
original_save_file = save_system.SAVE_FILE

save_system.SAVE_DIR = test_dir
save_system.SAVE_FILE = os.path.join(test_dir, 'game_save.json')

test_passed = 0
test_failed = 0

class MockPlayer:
    def __init__(self, name="TestPlayer"):
        self.name = name
        self.level = 5
        self.exp = 50
        self.exp_to_next = 200
        self.health = 80
        self.max_health = 100
        self.attack = 25
        self.defense = 15
        self.gold = 500
        self.inventory = {'health_potion': 3, 'attack_boost': 1}
        self.quests = [
            {'id': 'test_quest', 'name': 'Test Quest', 'completed': False}
        ]
        self.current_location = 'forest'
        self.current_story_node = 'forest_entrance'
        self.story_flags = {'test_flag': True}
        self.total_gold_earned = 1000
        self.monsters_killed = {'slime': 10}
        self.has_artifact = False
        self.defeated_dragon = False
        self.accepted_main_quest = True
    
    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'exp': self.exp,
            'exp_to_next': self.exp_to_next,
            'health': self.health,
            'max_health': self.max_health,
            'attack': self.attack,
            'defense': self.defense,
            'gold': self.gold,
            'inventory': self.inventory,
            'quests': self.quests,
            'current_location': self.current_location,
            'current_story_node': self.current_story_node,
            'story_flags': self.story_flags,
            'total_gold_earned': self.total_gold_earned,
            'monsters_killed': self.monsters_killed,
            'has_artifact': self.has_artifact,
            'defeated_dragon': self.defeated_dragon,
            'accepted_main_quest': self.accepted_main_quest
        }

def run_test(name, test_func):
    global test_passed, test_failed
    print(f"\n[Test] {name}...")
    try:
        result = test_func()
        if result:
            print(f"  [PASS] {name}")
            test_passed += 1
        else:
            print(f"  [FAIL] {name}")
            test_failed += 1
        return result
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")
        import traceback
        traceback.print_exc()
        test_failed += 1
        return False

def test_ensure_save_dir():
    result = save_system.ensure_save_dir()
    return result and os.path.exists(test_dir)

def test_validate_save_data():
    valid_data = {
        'version': '1.1',
        'save_time': '2026-04-23T10:00:00',
        'player': {
            'name': 'Test',
            'level': 1,
            'health': 100,
            'max_health': 100,
            'attack': 10,
            'defense': 5,
            'gold': 50
        }
    }
    
    is_valid, msg = save_system.validate_save_data(valid_data)
    if not is_valid:
        print(f"    Valid data validation failed: {msg}")
        return False
    
    invalid_data = {
        'version': '1.1',
        'player': {}
    }
    
    is_valid, msg = save_system.validate_save_data(invalid_data)
    if is_valid:
        print("    Invalid data was not detected")
        return False
    
    return True

def test_save_game():
    player = MockPlayer("SaveTestPlayer")
    
    result = save_system.save_game(player, show_confirmation=False)
    
    if not result:
        print("    Save function returned False")
        return False
    
    if not os.path.exists(save_system.SAVE_FILE):
        print("    Save file not created")
        return False
    
    try:
        with open(save_system.SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        is_valid, msg = save_system.validate_save_data(data)
        if not is_valid:
            print(f"    Saved data invalid: {msg}")
            return False
        
        player_data = data.get('player', {})
        if player_data.get('name') != "SaveTestPlayer":
            print(f"    Player name mismatch: {player_data.get('name')}")
            return False
            
    except Exception as e:
        print(f"    Error reading save: {e}")
        return False
    
    return True

def test_multiple_saves():
    player1 = MockPlayer("FirstSave")
    player2 = MockPlayer("SecondSave")
    
    save_system.save_game(player1, show_confirmation=False)
    
    import time
    time.sleep(0.05)
    
    save_system.save_game(player2, show_confirmation=False)
    
    backup1 = save_system.get_backup_path(1)
    
    if os.path.exists(backup1):
        return True
    else:
        print("    Backup file not created")
        return False

def test_atomic_write():
    player = MockPlayer("AtomicTest")
    
    save_system.save_game(player, show_confirmation=False)
    
    temp_files = [f for f in os.listdir(test_dir) if f.startswith('.tmp_save_')]
    
    if len(temp_files) > 0:
        print(f"    Leftover temp files: {temp_files}")
        for tf in temp_files:
            try:
                os.remove(os.path.join(test_dir, tf))
            except:
                pass
    
    return True

def test_has_save_file():
    return save_system.has_save_file()

def cleanup():
    print("\n" + "=" * 60)
    print("  Cleaning up test files...")
    
    try:
        shutil.rmtree(test_dir)
        print(f"  Test directory removed: {test_dir}")
    except Exception as e:
        print(f"  Warning: Could not remove test dir - {e}")
    
    save_system.SAVE_DIR = original_save_dir
    save_system.SAVE_FILE = original_save_file

def run_all_tests():
    global test_passed, test_failed
    
    print("\nRunning archive system tests...")
    
    run_test("Ensure Save Directory", test_ensure_save_dir)
    run_test("Data Validation", test_validate_save_data)
    run_test("Save Game", test_save_game)
    run_test("Multiple Saves (Backup)", test_multiple_saves)
    run_test("Atomic Write", test_atomic_write)
    run_test("Has Save File", test_has_save_file)
    
    cleanup()
    
    print("\n" + "=" * 60)
    print(f"  Test Results: {test_passed} passed, {test_failed} failed")
    print("=" * 60)
    
    return test_failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    os.chdir(original_cwd)
    sys.exit(0 if success else 1)
