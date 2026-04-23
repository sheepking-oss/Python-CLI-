from config import SHOP_ITEMS, ITEMS
from colors import print_color, color_text, print_item

def open_shop(player):
    while True:
        print("\n" + color_text("=" * 50, 'cyan'))
        print(color_text("  村庄商店", 'bold'))
        print(color_text("=" * 50, 'cyan'))
        print(f"  你的金币: {color_text(str(player.gold), 'yellow')}")
        print(color_text("-" * 50, 'cyan'))
        
        print_color("  商品列表:", 'yellow')
        
        for i, item_key in enumerate(SHOP_ITEMS, 1):
            item = ITEMS[item_key]
            print_color(f"\n  [{i}] ", 'yellow', end='')
            print_item(item_key, show_price=True)
        
        print(color_text("-" * 50, 'cyan'))
        print_color("  [0] 离开商店", 'yellow')
        
        choice = input("\n  选择要购买的商品: ").strip()
        
        if choice == '0':
            print_color("  欢迎下次光临！", 'green')
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(SHOP_ITEMS):
                item_key = SHOP_ITEMS[idx]
                item = ITEMS[item_key]
                price = item['price']
                
                if player.gold >= price:
                    player.gold -= price
                    player.add_item(item_key)
                    print_color(f"\n  购买了 {item['name']}！", 'green')
                    print_color(f"  花费了 {price} 金币。", 'yellow')
                else:
                    print_color(f"\n  金币不足！需要 {price} 金币，你只有 {player.gold} 金币。", 'red')
            else:
                print_color("  无效的选择！", 'red')
        except ValueError:
            print_color("  请输入有效的数字！", 'red')
