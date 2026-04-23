from config import ITEMS
from colors import print_color, print_item, color_text

def use_item(player, item_key):
    if not player.has_item(item_key):
        print_color("  你没有这个道具！", 'red')
        return False
    
    item = ITEMS.get(item_key)
    if not item:
        return False
    
    item_type = item['type']
    effect = item.get('effect', {})
    
    if item_type == 'consumable':
        if 'health' in effect:
            old_health = player.health
            player.heal(effect['health'])
            heal_amount = player.health - old_health
            print_color(f"  使用了 {item['name']}，恢复了 {heal_amount} 点生命值！", 'green')
            player.remove_item(item_key)
            return True
    
    elif item_type == 'permanent':
        if 'attack' in effect:
            player.attack += effect['attack']
            print_color(f"  使用了 {item['name']}，攻击力永久增加了 {effect['attack']} 点！", 'green')
        if 'defense' in effect:
            player.defense += effect['defense']
            print_color(f"  使用了 {item['name']}，防御力永久增加了 {effect['defense']} 点！", 'green')
        player.remove_item(item_key)
        return True
    
    elif item_type == 'combat':
        print_color(f"  {item['name']} 只能在战斗中使用！", 'yellow')
        return False
    
    return False

def use_combat_item(player, item_key):
    if not player.has_item(item_key):
        print_color("  你没有这个道具！", 'red')
        return 0
    
    item = ITEMS.get(item_key)
    if not item:
        return 0
    
    effect = item.get('effect', {})
    
    if item['type'] == 'combat' and 'damage' in effect:
        damage = effect['damage']
        print_color(f"  使用了 {item['name']}，造成了 {damage} 点伤害！", 'green')
        player.remove_item(item_key)
        return damage
    
    elif item['type'] == 'consumable':
        if 'health' in effect:
            old_health = player.health
            player.heal(effect['health'])
            heal_amount = player.health - old_health
            print_color(f"  使用了 {item['name']}，恢复了 {heal_amount} 点生命值！", 'green')
            player.remove_item(item_key)
            return 0
    
    return 0

def show_inventory(player):
    print("\n" + color_text("=" * 40, 'cyan'))
    print(color_text("  背包", 'bold'))
    print(color_text("=" * 40, 'cyan'))
    
    if not player.inventory:
        print_color("  背包是空的。", 'yellow')
        print(color_text("=" * 40, 'cyan') + "\n")
        return
    
    items_list = list(player.inventory.items())
    
    for i, (item_key, quantity) in enumerate(items_list, 1):
        print_color(f"\n  [{i}] ", 'yellow', end='')
        print_item(item_key, quantity)
    
    print(color_text("=" * 40, 'cyan'))
    
    while True:
        choice = input("\n  输入数字使用道具，或按 [0] 返回: ").strip()
        
        if choice == '0':
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(items_list):
                item_key, _ = items_list[idx]
                use_item(player, item_key)
                return
            else:
                print_color("  无效的选择！", 'red')
        except ValueError:
            print_color("  请输入有效的数字！", 'red')

def get_combat_items(player):
    combat_items = []
    for item_key, quantity in player.inventory.items():
        item = ITEMS.get(item_key)
        if item and (item['type'] == 'combat' or 
                      (item['type'] == 'consumable' and 'health' in item.get('effect', {}))):
            combat_items.append((item_key, quantity))
    return combat_items
