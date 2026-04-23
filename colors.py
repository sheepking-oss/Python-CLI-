from config import COLORS
import os

if os.name == 'nt':
    os.system('color')

def color_text(text, color_name):
    if color_name in COLORS:
        return f"{COLORS[color_name]}{text}{COLORS['reset']}"
    return text

def print_color(text, color_name, end='\n'):
    print(color_text(text, color_name), end=end)

def print_health(current, max_health, width=20):
    bar_width = width - 2
    filled = int((current / max_health) * bar_width)
    
    if current > max_health * 0.6:
        bar_color = 'green'
    elif current > max_health * 0.3:
        bar_color = 'yellow'
    else:
        bar_color = 'red'
    
    bar = '[' + '█' * filled + '░' * (bar_width - filled) + ']'
    return color_text(bar, bar_color)

def print_stats(player):
    print("\n" + color_text("=" * 40, 'cyan'))
    print(color_text(f"  {player.name} - 等级 {player.level}", 'bold'))
    print(color_text("=" * 40, 'cyan'))
    
    print(f"  生命值: {print_health(player.health, player.max_health)} {player.health}/{player.max_health}")
    print(f"  攻击力: {color_text(str(player.attack), 'red')}")
    print(f"  防御力: {color_text(str(player.defense), 'blue')}")
    print(f"  经验值: {color_text(f'{player.exp}/{player.exp_to_next}', 'yellow')}")
    print(f"  金币: {color_text(str(player.gold), 'yellow')}")
    print(color_text("=" * 40, 'cyan') + "\n")

def print_choices(choices):
    for i, choice in enumerate(choices, 1):
        text = choice.get('text', str(choice))
        print_color(f"  [{i}] {text}", 'yellow')
    print()

def print_item(item_key, quantity=1, show_price=False):
    from config import ITEMS
    item = ITEMS.get(item_key)
    if not item:
        return
    
    name = item['name']
    desc = item['description']
    price = item.get('price', 0)
    
    line = f"  {name}"
    if quantity > 1:
        line += f" x{quantity}"
    
    if show_price and price > 0:
        line += f" - {price} 金币"
    
    print_color(line, 'green')
    print_color(f"    {desc}", 'white')

def print_monster(monster_key, show_stats=False):
    from config import MONSTERS
    monster = MONSTERS.get(monster_key)
    if not monster:
        return
    
    name = monster['name']
    desc = monster['description']
    
    print_color(f"\n  {name} 出现了！", 'red')
    print_color(f"    {desc}", 'white')
    
    if show_stats:
        print_color(f"    生命值: {monster['health']}", 'red')
        print_color(f"    攻击力: {monster['attack']}", 'red')
        print_color(f"    防御力: {monster['defense']}", 'blue')

def print_quest(quest, show_progress=True):
    status = color_text("[已完成]", 'green') if quest['completed'] else color_text("[进行中]", 'yellow')
    print_color(f"\n  {quest['name']} {status}", 'cyan')
    print_color(f"    {quest['description']}", 'white')
    
    if show_progress and not quest['completed']:
        progress = quest.get('progress', 0)
        target = quest.get('target_count', quest.get('target', 0))
        if isinstance(target, int) and target > 0:
            print_color(f"    进度: {progress}/{target}", 'yellow')
    
    print_color(f"    奖励: {quest['gold_reward']} 金币, {quest['exp_reward']} 经验", 'green')

def print_title():
    title = """
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ████████╗███████╗██╗  ██╗████████╗     █████╗ ██████╗    ║
║   ╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝    ██╔══██╗██╔══██╗   ║
║      ██║   █████╗   ╚███╔╝    ██║       ███████║██║  ██║   ║
║      ██║   ██╔══╝   ██╔██╗    ██║       ██╔══██║██║  ██║   ║
║      ██║   ███████╗██╔╝ ██╗   ██║       ██║  ██║██████╔╝   ║
║      ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═════╝    ║
║                                                                ║
║                    文 字 冒 险 游 戏                           ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(color_text(title, 'cyan'))

def print_menu():
    print("\n" + color_text("=" * 50, 'cyan'))
    print(color_text("  主菜单", 'bold'))
    print(color_text("=" * 50, 'cyan'))
    print_choices([
        {'text': '开始新游戏'},
        {'text': '读取存档'},
        {'text': '游戏说明'},
        {'text': '退出游戏'}
    ])

def print_battle_status(player, monster, monster_health):
    print("\n" + color_text("-" * 40, 'cyan'))
    print(f"  {color_text(player.name, 'green')} vs {color_text(monster['name'], 'red')}")
    print(color_text("-" * 40, 'cyan'))
    
    print(f"  {player.name}: {print_health(player.health, player.max_health)} {player.health}/{player.max_health}")
    print(f"  {monster['name']}: {print_health(monster_health, monster['health'])} {monster_health}/{monster['health']}")
    print(color_text("-" * 40, 'cyan') + "\n")
