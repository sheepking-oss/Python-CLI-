import random
from config import MONSTERS, ITEMS
from colors import print_color, color_text, print_battle_status, print_monster
from inventory import get_combat_items, use_combat_item

def calculate_damage(attacker_attack, defender_defense):
    base_damage = attacker_attack - defender_defense // 2
    variance = random.randint(-2, 2)
    return max(1, base_damage + variance)

def get_random_monster(location_monsters):
    if not location_monsters:
        return None
    
    monster_key = random.choice(location_monsters)
    monster_data = MONSTERS.get(monster_key)
    
    if monster_data:
        return monster_key, monster_data
    return None

def encounter_monster(location_data):
    if random.random() < location_data.get('encounter_chance', 0):
        monsters = location_data.get('monsters', [])
        return get_random_monster(monsters)
    return None

def start_combat(player, monster_key, monster_data, is_boss=False):
    monster_health = monster_data['health']
    
    print_monster(monster_key, show_stats=True)
    
    if is_boss:
        print_color("\n  ⚔️ BOSS战开始！ ⚔️", 'red')
    
    while player.is_alive() and monster_health > 0:
        print_battle_status(player, monster_data, monster_health)
        
        print_color("  你的回合！", 'yellow')
        print_color("  [1] 普通攻击", 'yellow')
        print_color("  [2] 使用道具", 'yellow')
        print_color("  [3] 尝试逃跑", 'yellow')
        
        choice = input("\n  选择行动: ").strip()
        
        if choice == '1':
            damage = calculate_damage(player.attack, monster_data['defense'])
            monster_health -= damage
            print_color(f"\n  你对 {monster_data['name']} 造成了 {damage} 点伤害！", 'green')
            
            if monster_health <= 0:
                break
            
            monster_damage = calculate_damage(monster_data['attack'], player.defense)
            actual_damage = player.take_damage(monster_damage)
            print_color(f"  {monster_data['name']} 对你造成了 {actual_damage} 点伤害！", 'red')
        
        elif choice == '2':
            combat_items = get_combat_items(player)
            
            if not combat_items:
                print_color("  你没有可用的战斗道具！", 'yellow')
                continue
            
            print("\n" + color_text("-" * 40, 'cyan'))
            print_color("  可用道具:", 'yellow')
            
            for i, (item_key, quantity) in enumerate(combat_items, 1):
                item = ITEMS[item_key]
                print_color(f"  [{i}] {item['name']} x{quantity}", 'green')
            
            print_color("  [0] 取消", 'yellow')
            print(color_text("-" * 40, 'cyan'))
            
            item_choice = input("\n  选择道具: ").strip()
            
            if item_choice == '0':
                continue
            
            try:
                idx = int(item_choice) - 1
                if 0 <= idx < len(combat_items):
                    item_key, _ = combat_items[idx]
                    item = ITEMS[item_key]
                    
                    if item['type'] == 'combat':
                        damage = use_combat_item(player, item_key)
                        if damage > 0:
                            monster_health -= damage
                            if monster_health <= 0:
                                break
                    else:
                        use_combat_item(player, item_key)
                    
                    monster_damage = calculate_damage(monster_data['attack'], player.defense)
                    actual_damage = player.take_damage(monster_damage)
                    print_color(f"  {monster_data['name']} 对你造成了 {actual_damage} 点伤害！", 'red')
                else:
                    print_color("  无效的选择！", 'red')
            except ValueError:
                print_color("  请输入有效的数字！", 'red')
        
        elif choice == '3':
            if is_boss:
                print_color("  无法从 BOSS 战中逃跑！", 'red')
                continue
            
            escape_chance = 0.5
            if random.random() < escape_chance:
                print_color("  你成功逃跑了！", 'green')
                return 'escaped'
            else:
                print_color("  逃跑失败！", 'red')
                monster_damage = calculate_damage(monster_data['attack'], player.defense)
                actual_damage = player.take_damage(monster_damage)
                print_color(f"  {monster_data['name']} 对你造成了 {actual_damage} 点伤害！", 'red')
        
        else:
            print_color("  无效的选择！", 'red')
    
    if player.is_alive() and monster_health <= 0:
        gold_reward = monster_data['gold_reward']
        exp_reward = monster_data['exp_reward']
        
        player.gain_gold(gold_reward)
        leveled_up = player.gain_exp(exp_reward)
        player.kill_monster(monster_key)
        
        print_color(f"\n  你击败了 {monster_data['name']}！", 'green')
        print_color(f"  获得 {gold_reward} 金币和 {exp_reward} 经验值！", 'yellow')
        
        if leveled_up:
            print_color(f"\n  恭喜！你升级到了 {player.level} 级！", 'cyan')
            print_color(f"  生命值上限、攻击力和防御力都提升了！", 'cyan')
        
        return 'victory'
    else:
        print_color(f"\n  你被 {monster_data['name']} 击败了...", 'red')
        return 'defeat'
