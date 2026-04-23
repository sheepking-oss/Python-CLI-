import os
import json
from config import SAVE_DIR, SAVE_FILE
from player import Player
from colors import print_color, color_text

def ensure_save_dir():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def save_game(player, show_confirmation=True):
    ensure_save_dir()
    
    try:
        save_data = {
            'player': player.to_dict(),
            'version': '1.0'
        }
        
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        if show_confirmation:
            print_color("\n  游戏保存成功！", 'green')
            print_color("  进度已保存，你可以安全退出游戏。", 'cyan')
        return True
    
    except Exception as e:
        print_color(f"\n  保存失败: {e}", 'red')
        return False

def save_game_with_menu(player):
    from colors import color_text, print_color
    
    print("\n" + color_text("=" * 50, 'cyan'))
    print(color_text("  保存游戏", 'bold'))
    print(color_text("=" * 50, 'cyan'))
    
    success = save_game(player, show_confirmation=False)
    
    if success:
        print_color("\n  ✓ 游戏保存成功！", 'green')
        print_color("  当前进度已保存。", 'cyan')
        
        print("\n" + color_text("-" * 50, 'cyan'))
        print_color("  保存后操作:", 'yellow')
        print_color("  [1] 继续当前游戏", 'yellow')
        print_color("  [2] 返回游戏主菜单", 'yellow')
        print_color("  [3] 退出游戏", 'yellow')
        print(color_text("-" * 50, 'cyan'))
        
        while True:
            choice = input("\n  请选择 [1-3]: ").strip()
            
            if choice == '1':
                print_color("\n  继续游戏...", 'cyan')
                return 'continue'
            
            elif choice == '2':
                print_color("\n  返回主菜单...", 'cyan')
                return 'main_menu'
            
            elif choice == '3':
                print_color("\n  感谢游玩！再见！", 'cyan')
                import sys
                sys.exit(0)
            
            else:
                print_color("  无效的选择，请输入 1-3。", 'red')
    else:
        print_color("\n  保存失败！请检查文件权限或磁盘空间。", 'red')
        input("\n  按回车键继续...")
        return 'continue'

def load_game():
    if not os.path.exists(SAVE_FILE):
        print_color("\n  没有找到存档文件！", 'yellow')
        return None
    
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        player_data = save_data.get('player', {})
        player = Player.from_dict(player_data)
        
        print_color("\n  游戏读取成功！", 'green')
        return player
    
    except Exception as e:
        print_color(f"\n  读取失败: {e}", 'red')
        return None

def has_save_file():
    return os.path.exists(SAVE_FILE)

def delete_save():
    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
            print_color("\n  存档已删除。", 'yellow')
            return True
        except Exception as e:
            print_color(f"\n  删除失败: {e}", 'red')
            return False
    else:
        print_color("\n  没有找到存档文件。", 'yellow')
        return False

def show_save_info():
    if not os.path.exists(SAVE_FILE):
        print_color("\n  没有找到存档文件。", 'yellow')
        return
    
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        player_data = save_data.get('player', {})
        
        print("\n" + color_text("=" * 40, 'cyan'))
        print(color_text("  存档信息", 'bold'))
        print(color_text("=" * 40, 'cyan'))
        print(f"  角色名: {player_data.get('name', '未知')}")
        print(f"  等级: {player_data.get('level', 1)}")
        print(f"  金币: {player_data.get('gold', 0)}")
        print(f"  当前位置: {player_data.get('current_location', '未知')}")
        print(color_text("=" * 40, 'cyan'))
    
    except Exception as e:
        print_color(f"\n  读取存档信息失败: {e}", 'red')
