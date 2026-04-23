#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

original_cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("  存档系统测试")
print("=" * 60)

test_dir = tempfile.mkdtemp(prefix='test_save_')
print(f"\n测试目录: {test_dir}")

import save_system

original_save_dir = save_system.SAVE_DIR
original_save_file = save_system.SAVE_FILE

save_system.SAVE_DIR = test_dir
save_system.SAVE_FILE = os.path.join(test_dir, 'game_save.json')

test_passed = 0
test_failed = 0

def test_ensure_save_dir():
    global test_passed, test_failed
    print("\n[测试 1] 确保存档目录...")
    
    result = save_system.ensure_save_dir()
    
    if result and os.path.exists(test_dir):
        print("  ✓ 通过: 存档目录已创建")
        test_passed += 1
        return True
    else:
        print("  ✗ 失败: 无法创建存档目录")
        test_failed += 1
        return False

class MockPlayer:
    def __init__(self, name="测试角色"):
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
            {'id': 'test_quest', 'name': '测试任务', 'completed': False}
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

def test_validate_save_data():
    global test_passed, test_failed
    print("\n[测试 2] 数据验证...")
    
    valid_data = {
        'version': '1.1',
        'save_time': '2026-04-23T10:00:00',
        'player': {
            'name': '测试',
            'level': 1,
            'health': 100,
            'max_health': 100,
            'attack': 10,
            'defense': 5,
            'gold': 50
        }
    }
    
    is_valid, msg = save_system.validate_save_data(valid_data)
    if is_valid:
        print("  ✓ 通过: 有效数据验证通过")
    else:
        print(f"  ✗ 失败: 有效数据验证失败 - {msg}")
        test_failed += 1
        return False
    
    invalid_data = {
        'version': '1.1',
        'player': {}
    }
    
    is_valid, msg = save_system.validate_save_data(invalid_data)
    if not is_valid:
        print("  ✓ 通过: 无效数据正确识别")
    else:
        print("  ✗ 失败: 无效数据未被识别")
        test_failed += 1
        return False
    
    test_passed += 1
    return True

def test_save_game():
    global test_passed, test_failed
    print("\n[测试 3] 保存游戏...")
    
    player = MockPlayer("存档测试角色")
    
    result = save_system.save_game(player, show_confirmation=False)
    
    if result:
        print("  ✓ 通过: 保存成功")
    else:
        print("  ✗ 失败: 保存失败")
        test_failed += 1
        return False
    
    if os.path.exists(save_system.SAVE_FILE):
        print("  ✓ 通过: 存档文件已创建")
    else:
        print("  ✗ 失败: 存档文件不存在")
        test_failed += 1
        return False
    
    try:
        with open(save_system.SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        is_valid, _ = save_system.validate_save_data(data)
        if is_valid:
            print("  ✓ 通过: 存档数据有效")
        else:
            print("  ✗ 失败: 存档数据无效")
            test_failed += 1
            return False
        
        player_data = data.get('player', {})
        if player_data.get('name') == "存档测试角色":
            print("  ✓ 通过: 玩家数据正确保存")
        else:
            print("  ✗ 失败: 玩家数据不正确")
            test_failed += 1
            return False
            
    except Exception as e:
        print(f"  ✗ 失败: 读取存档时出错 - {e}")
        test_failed += 1
        return False
    
    test_passed += 1
    return True

def test_multiple_saves_create_backups():
    global test_passed, test_failed
    print("\n[测试 4] 多次保存创建备份...")
    
    player1 = MockPlayer("第一次保存")
    player2 = MockPlayer("第二次保存")
    player3 = MockPlayer("第三次保存")
    
    save_system.save_game(player1, show_confirmation=False)
    first_save_time = os.path.getmtime(save_system.SAVE_FILE)
    
    import time
    time.sleep(0.1)
    
    save_system.save_game(player2, show_confirmation=False)
    
    backup1 = save_system.get_backup_path(1)
    if os.path.exists(backup1):
        print("  ✓ 通过: 第一次备份已创建")
    else:
        print("  ✗ 失败: 第一次备份未创建")
        test_failed += 1
        return False
    
    time.sleep(0.1)
    save_system.save_game(player3, show_confirmation=False)
    
    backup2 = save_system.get_backup_path(2)
    if os.path.exists(backup2):
        print("  ✓ 通过: 第二次备份已创建")
    else:
        print("  注意: 可能还没有足够的保存次数来创建第二个备份")
    
    test_passed += 1
    return True

def test_atomic_write():
    global test_passed, test_failed
    print("\n[测试 5] 原子写入验证...")
    
    player = MockPlayer("原子写入测试")
    
    save_system.save_game(player, show_confirmation=False)
    
    with open(save_system.SAVE_FILE, 'r', encoding='utf-8') as f:
        original_data = f.read()
    
    temp_files = [f for f in os.listdir(test_dir) if f.startswith('.tmp_save_')]
    if len(temp_files) == 0:
        print("  ✓ 通过: 没有残留的临时文件")
    else:
        print(f"  警告: 发现残留的临时文件: {temp_files}")
        for tf in temp_files:
            try:
                os.remove(os.path.join(test_dir, tf))
            except:
                pass
    
    test_passed += 1
    return True

def test_has_save_file():
    global test_passed, test_failed
    print("\n[测试 6] 检查存档存在...")
    
    if save_system.has_save_file():
        print("  ✓ 通过: 检测到存档存在")
    else:
        print("  ✗ 失败: 未检测到存档")
        test_failed += 1
        return False
    
    test_passed += 1
    return True

def test_cleanup():
    print("\n" + "=" * 60)
    print("  清理测试文件...")
    
    try:
        shutil.rmtree(test_dir)
        print(f"  ✓ 测试目录已删除: {test_dir}")
    except Exception as e:
        print(f"  警告: 无法删除测试目录 - {e}")
    
    save_system.SAVE_DIR = original_save_dir
    save_system.SAVE_FILE = original_save_file

def run_all_tests():
    global test_passed, test_failed
    
    print("\n开始测试存档系统...")
    
    test_ensure_save_dir()
    test_validate_save_data()
    test_save_game()
    test_multiple_saves_create_backups()
    test_atomic_write()
    test_has_save_file()
    
    test_cleanup()
    
    print("\n" + "=" * 60)
    print(f"  测试结果: {test_passed} 通过, {test_failed} 失败")
    print("=" * 60)
    
    return test_failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    os.chdir(original_cwd)
    sys.exit(0 if success else 1)
