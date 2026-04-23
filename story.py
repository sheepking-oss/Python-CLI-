import random
from config import STORY_NODES, ENDINGS, MAP_LOCATIONS, MONSTERS
from colors import print_color, color_text, print_choices
from combat import start_combat, encounter_monster
from shop import open_shop

def get_story_node(node_key):
    return STORY_NODES.get(node_key)

def show_ending(ending_key):
    ending = ENDINGS.get(ending_key)
    if not ending:
        return
    
    print("\n" + color_text("=" * 60, 'magenta'))
    print(color_text(f"  结局: {ending['title']}", 'bold'))
    print(color_text("=" * 60, 'magenta'))
    print()
    
    for line in ending['description'].split('。'):
        if line.strip():
            print_color(f"  {line}。", 'white')
    
    print()
    print_color("  " + "=" * 50, 'magenta')
    print_color("  尾声", 'bold')
    print_color("  " + "=" * 50, 'magenta')
    print()
    
    for line in ending['epilogue'].split('。'):
        if line.strip():
            print_color(f"  {line}。", 'white')
    
    print("\n" + color_text("=" * 60, 'magenta'))
    input("\n  按回车键返回主菜单...")

def process_story_choice(player, choice):
    next_node = choice.get('next')
    reward = choice.get('reward', {})
    flag = choice.get('flag')
    requires_flag = choice.get('requires_flag')
    
    if requires_flag and not player.has_flag(requires_flag):
        print_color("  你没有足够的条件选择这个选项...", 'yellow')
        return None
    
    if reward:
        if 'gold' in reward:
            player.gain_gold(reward['gold'])
            print_color(f"  获得了 {reward['gold']} 金币！", 'yellow')
        if 'attack' in reward:
            player.attack += reward['attack']
            print_color(f"  攻击力增加了 {reward['attack']} 点！", 'green')
        if 'defense' in reward:
            player.defense += reward['defense']
            print_color(f"  防御力增加了 {reward['defense']} 点！", 'green')
    
    if flag:
        player.set_flag(flag, True)
        print_color(f"  剧情触发: {flag}", 'cyan')
    
    return next_node

def process_action(player, action):
    if action == 'open_shop':
        open_shop(player)
        return 'village_entrance'
    
    elif action == 'explore_forest':
        return explore_location(player, 'forest')
    
    elif action == 'explore_mountain':
        return explore_location(player, 'mountain')
    
    elif action == 'free_explore':
        return free_explore_mode(player)
    
    elif action == 'boss_battle':
        return boss_battle(player, 'dark_lord')
    
    elif action == 'final_boss_boosted':
        monster_data = MONSTERS['dark_lord'].copy()
        monster_data['health'] = int(monster_data['health'] * 1.5)
        monster_data['attack'] = int(monster_data['attack'] * 1.3)
        return boss_battle_with_data(player, 'dark_lord', monster_data)
    
    return None

def explore_location(player, location_key):
    location = MAP_LOCATIONS.get(location_key)
    if not location:
        return player.current_story_node
    
    print_color(f"\n  你正在 {location['name']} 探索...", 'cyan')
    
    encounter = encounter_monster(location)
    
    if encounter:
        monster_key, monster_data = encounter
        result = start_combat(player, monster_key, monster_data)
        
        if result == 'defeat':
            show_ending('fallen_hero')
            return 'game_over'
        
        elif result == 'victory':
            if monster_key == 'dragon' and not player.defeated_dragon:
                return 'defeated_dragon'
            
            if random.random() < 0.1 and not player.has_artifact:
                if monster_key in ['dragon', 'orc', 'skeleton']:
                    return 'found_artifact'
    
    else:
        print_color("  这片区域很安静...", 'yellow')
    
    return 'continue_adventure'

def free_explore_mode(player):
    while True:
        location = MAP_LOCATIONS.get(player.current_location, MAP_LOCATIONS['village'])
        
        print("\n" + color_text("=" * 50, 'cyan'))
        print(color_text(f"  当前位置: {location['name']}", 'bold'))
        print(color_text("=" * 50, 'cyan'))
        print_color(f"  {location['description']}", 'white')
        print(color_text("-" * 50, 'cyan'))
        
        print_color("  你可以:", 'yellow')
        print_color("  [1] 探索当前区域", 'yellow')
        print_color("  [2] 查看背包", 'yellow')
        print_color("  [3] 查看任务", 'yellow')
        print_color("  [4] 查看角色状态", 'yellow')
        print_color("  [5] 保存游戏", 'yellow')
        
        connected = location.get('connected', [])
        for i, loc_key in enumerate(connected, 6):
            loc = MAP_LOCATIONS.get(loc_key)
            if loc:
                print_color(f"  [{i}] 前往 {loc['name']}", 'yellow')
        
        if location.get('has_shop'):
            print_color(f"  [{len(connected) + 6}] 进入商店", 'yellow')
        
        print_color("  [0] 返回剧情模式", 'yellow')
        
        choice = input("\n  选择行动: ").strip()
        
        if choice == '0':
            return 'continue_adventure'
        
        elif choice == '1':
            result = explore_location(player, player.current_location)
            if result == 'game_over':
                return 'game_over'
        
        elif choice == '2':
            from inventory import show_inventory
            show_inventory(player)
        
        elif choice == '3':
            from quest_system import show_quests
            show_quests(player)
        
        elif choice == '4':
            from colors import print_stats
            print_stats(player)
        
        elif choice == '5':
            from save_system import save_game_with_menu
            result = save_game_with_menu(player)
            if result == 'main_menu':
                return 'main_menu'
        
        elif choice == str(len(connected) + 6) and location.get('has_shop'):
            open_shop(player)
        
        else:
            try:
                idx = int(choice) - 6
                if 0 <= idx < len(connected):
                    player.current_location = connected[idx]
                    new_loc = MAP_LOCATIONS.get(connected[idx])
                    print_color(f"  你来到了 {new_loc['name']}。", 'green')
                else:
                    print_color("  无效的选择！", 'red')
            except ValueError:
                print_color("  请输入有效的数字！", 'red')

def boss_battle(player, boss_key):
    monster_data = MONSTERS.get(boss_key)
    return boss_battle_with_data(player, boss_key, monster_data)

def boss_battle_with_data(player, boss_key, monster_data):
    if not monster_data:
        return 'continue_adventure'
    
    result = start_combat(player, boss_key, monster_data, is_boss=True)
    
    if result == 'victory':
        if boss_key == 'dark_lord':
            if player.has_artifact:
                return 'true_hero'
            else:
                return 'victorious_warrior'
    
    elif result == 'defeat':
        show_ending('fallen_hero')
        return 'game_over'
    
    return 'continue_adventure'

def run_story(player):
    current_node = player.current_story_node
    
    while current_node:
        node = get_story_node(current_node)
        
        if not node:
            print_color("  剧情节点不存在，返回主菜单...", 'yellow')
            return
        
        if 'ending' in node:
            show_ending(node['ending'])
            return
        
        print("\n" + color_text("-" * 60, 'cyan'))
        for paragraph in node['text'].split('。'):
            if paragraph.strip():
                print_color(f"  {paragraph}。", 'white')
        print(color_text("-" * 60, 'cyan'))
        
        action = node.get('action')
        if action:
            result = process_action(player, action)
            if result == 'game_over':
                return
            if result:
                current_node = result
                player.current_story_node = current_node
            continue
        
        choices = node.get('choices', [])
        
        if not choices:
            print_color("  剧情结束，返回自由探索...", 'yellow')
            return
        
        available_choices = []
        for choice in choices:
            requires_flag = choice.get('requires_flag')
            if not requires_flag or player.has_flag(requires_flag):
                available_choices.append(choice)
        
        print_color("\n  你的选择:", 'yellow')
        print_choices(available_choices)
        
        while True:
            choice_input = input("  选择: ").strip()
            
            try:
                choice_idx = int(choice_input) - 1
                if 0 <= choice_idx < len(available_choices):
                    next_node = process_story_choice(player, available_choices[choice_idx])
                    if next_node:
                        current_node = next_node
                        player.current_story_node = current_node
                    break
                else:
                    print_color("  无效的选择！", 'red')
            except ValueError:
                print_color("  请输入有效的数字！", 'red')
