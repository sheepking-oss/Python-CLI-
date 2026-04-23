import os
import json
from config import SAVE_DIR, SAVE_FILE
from player import Player
from colors import print_color, color_text

def ensure_save_dir():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def save_game(player):
    ensure_save_dir()
    
    try:
        save_data = {
            'player': player.to_dict(),
            'version': '1.0'
        }
        
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print_color("\n  游戏保存成功！", 'green')
        return True
    
    except Exception as e:
        print_color(f"\n  保存失败: {e}", 'red')
        return False

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
