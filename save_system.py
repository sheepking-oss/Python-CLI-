import os
import json
import shutil
import tempfile
import time
from datetime import datetime

try:
    from config import SAVE_DIR, SAVE_FILE
except ImportError:
    SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saves')
    SAVE_FILE = os.path.join(SAVE_DIR, 'game_save.json')

try:
    from player import Player
except ImportError:
    Player = None

try:
    from colors import print_color, color_text
except ImportError:
    def print_color(text, color_name, end='\n'):
        print(text, end=end)
    
    def color_text(text, color_name):
        return text

SAVE_VERSION = '1.1'
MAX_BACKUPS = 5

def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def ensure_save_dir():
    try:
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR, exist_ok=True)
        return True
    except Exception as e:
        print_color(f"  创建存档目录失败: {e}", 'red')
        return False

def get_backup_path(backup_index=0):
    if backup_index == 0:
        return SAVE_FILE
    return f"{SAVE_FILE}.bak{backup_index}"

def rotate_backups():
    try:
        if not os.path.exists(SAVE_FILE):
            return
        
        for i in range(MAX_BACKUPS - 1, 0, -1):
            old_backup = get_backup_path(i)
            new_backup = get_backup_path(i + 1)
            
            if os.path.exists(old_backup):
                if os.path.exists(new_backup):
                    os.remove(new_backup)
                shutil.copy2(old_backup, new_backup)
        
        first_backup = get_backup_path(1)
        if os.path.exists(first_backup):
            os.remove(first_backup)
        shutil.copy2(SAVE_FILE, first_backup)
        
    except Exception as e:
        print_color(f"  存档备份时出错: {e}", 'yellow')

def validate_save_data(data):
    if not isinstance(data, dict):
        return False, "存档数据格式错误"
    
    if 'version' not in data:
        return False, "缺少版本信息"
    
    if 'player' not in data:
        return False, "缺少玩家数据"
    
    player_data = data['player']
    if not isinstance(player_data, dict):
        return False, "玩家数据格式错误"
    
    required_fields = ['name', 'level', 'health', 'max_health', 'attack', 'defense', 'gold']
    for field in required_fields:
        if field not in player_data:
            return False, f"缺少必要字段: {field}"
    
    return True, "数据验证通过"

def save_game(player, show_confirmation=True):
    if Player and not isinstance(player, Player):
        if show_confirmation:
            print_color("\n  错误: 无效的玩家数据！", 'red')
        return False
    
    if not ensure_save_dir():
        return False
    
    try:
        player_dict = player.to_dict()
        
        save_data = {
            'version': SAVE_VERSION,
            'save_time': datetime.now().isoformat(),
            'player': player_dict
        }
        
        is_valid, _ = validate_save_data(save_data)
        if not is_valid:
            if show_confirmation:
                print_color("\n  错误: 生成的存档数据无效！", 'red')
            return False
        
        temp_fd, temp_path = tempfile.mkstemp(
            dir=SAVE_DIR,
            prefix='.tmp_save_',
            suffix='.json'
        )
        os.close(temp_fd)
        
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2, sort_keys=False)
                f.flush()
                os.fsync(f.fileno())
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                verify_data = json.load(f)
            is_valid, _ = validate_save_data(verify_data)
            if not is_valid:
                raise Exception("写入的数据验证失败")
            
            if os.path.exists(SAVE_FILE):
                rotate_backups()
            
            if os.name == 'nt' and os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
            shutil.move(temp_path, SAVE_FILE)
            
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    final_verify = json.load(f)
                is_valid, _ = validate_save_data(final_verify)
                if not is_valid:
                    raise Exception("最终验证失败")
            else:
                raise Exception("存档文件不存在")
            
            if show_confirmation:
                print_color("\n  ✓ 游戏保存成功！", 'green')
                save_time = save_data.get('save_time', '未知')
                print_color(f"  保存时间: {save_time}", 'cyan')
                print_color(f"  存档位置: {SAVE_FILE}", 'cyan')
            
            return True
            
        except Exception as e:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            raise e
            
    except Exception as e:
        if show_confirmation:
            print_color(f"\n  ✗ 保存失败: {e}", 'red')
            import traceback
            traceback.print_exc()
        return False

def save_game_with_menu(player):
    print("\n" + color_text("=" * 50, 'cyan'))
    print(color_text("  保存游戏", 'bold'))
    print(color_text("=" * 50, 'cyan'))
    
    success = save_game(player, show_confirmation=False)
    
    if success:
        print_color("\n  ✓ 游戏保存成功！", 'green')
        print_color("  当前进度已保存到本地文件。", 'cyan')
        
        if os.path.exists(SAVE_FILE):
            try:
                file_size = os.path.getsize(SAVE_FILE)
                mod_time = datetime.fromtimestamp(os.path.getmtime(SAVE_FILE))
                print_color(f"  文件大小: {file_size} 字节", 'cyan')
                print_color(f"  修改时间: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}", 'cyan')
            except:
                pass
        
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
        print_color("\n  ✗ 保存失败！", 'red')
        print_color("  请检查以下内容:", 'yellow')
        print_color("  • 磁盘空间是否充足", 'yellow')
        print_color("  • 文件写入权限是否正常", 'yellow')
        print_color("  • 存档目录是否存在", 'yellow')
        input("\n  按回车键继续...")
        return 'continue'

def try_load_from_backups():
    for i in range(1, MAX_BACKUPS + 1):
        backup_path = get_backup_path(i)
        if os.path.exists(backup_path):
            try:
                with open(backup_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                is_valid, msg = validate_save_data(data)
                if is_valid:
                    print_color(f"\n  正在从备份恢复存档 (备份 #{i})...", 'yellow')
                    return data, backup_path
            except:
                continue
    
    return None, None

def load_game():
    if not os.path.exists(SAVE_FILE):
        print_color("\n  没有找到主存档文件...", 'yellow')
        
        backup_data, backup_path = try_load_from_backups()
        if backup_data:
            print_color(f"  发现可用的备份存档: {backup_path}", 'green')
            confirm = input("\n  是否从备份恢复？(y/n): ").strip().lower()
            if confirm == 'y':
                try:
                    shutil.copy2(backup_path, SAVE_FILE)
                    print_color("  备份已恢复到主存档！", 'green')
                except Exception as e:
                    print_color(f"  恢复备份失败: {e}", 'red')
                    return None
            else:
                return None
        else:
            print_color("\n  没有找到任何存档文件。", 'yellow')
            return None
    
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        is_valid, validate_msg = validate_save_data(save_data)
        if not is_valid:
            print_color(f"\n  存档数据验证失败: {validate_msg}", 'red')
            print_color("  尝试从备份恢复...", 'yellow')
            
            backup_data, backup_path = try_load_from_backups()
            if backup_data:
                confirm = input(f"\n  是否从备份 {backup_path} 恢复？(y/n): ").strip().lower()
                if confirm == 'y':
                    save_data = backup_data
                    try:
                        shutil.copy2(backup_path, SAVE_FILE)
                        print_color("  备份已恢复！", 'green')
                    except:
                        pass
                else:
                    return None
            else:
                print_color("  没有可用的备份存档。", 'yellow')
                return None
        
        player_data = save_data.get('player', {})
        
        if Player:
            player = Player.from_dict(player_data)
        else:
            player = player_data
        
        save_time = save_data.get('save_time', '未知')
        version = save_data.get('version', '未知')
        
        print_color("\n  ✓ 游戏读取成功！", 'green')
        print_color(f"  存档版本: {version}", 'cyan')
        print_color(f"  保存时间: {save_time}", 'cyan')
        
        return player
    
    except json.JSONDecodeError as e:
        print_color(f"\n  存档文件格式错误: {e}", 'red')
        print_color("  文件可能已损坏。", 'yellow')
        
        backup_data, backup_path = try_load_from_backups()
        if backup_data:
            confirm = input(f"\n  是否尝试从备份恢复？(y/n): ").strip().lower()
            if confirm == 'y':
                try:
                    shutil.copy2(backup_path, SAVE_FILE)
                    print_color("  已从备份恢复存档，请重新读取。", 'green')
                except:
                    pass
        return None
    
    except Exception as e:
        print_color(f"\n  读取失败: {e}", 'red')
        import traceback
        traceback.print_exc()
        return None

def has_save_file():
    if os.path.exists(SAVE_FILE):
        return True
    
    for i in range(1, MAX_BACKUPS + 1):
        if os.path.exists(get_backup_path(i)):
            return True
    
    return False

def has_main_save_file():
    return os.path.exists(SAVE_FILE)

def delete_save():
    deleted_count = 0
    
    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
            deleted_count += 1
            print_color("  主存档已删除。", 'yellow')
        except Exception as e:
            print_color(f"  删除主存档失败: {e}", 'red')
    
    for i in range(1, MAX_BACKUPS + 1):
        backup_path = get_backup_path(i)
        if os.path.exists(backup_path):
            try:
                os.remove(backup_path)
                deleted_count += 1
            except:
                pass
    
    if deleted_count > 0:
        print_color(f"  共删除 {deleted_count} 个存档文件。", 'yellow')
        return True
    else:
        print_color("  没有找到存档文件。", 'yellow')
        return False

def show_save_info():
    print("\n" + color_text("=" * 50, 'cyan'))
    print(color_text("  存档信息", 'bold'))
    print(color_text("=" * 50, 'cyan'))
    
    found_saves = []
    
    if os.path.exists(SAVE_FILE):
        found_saves.append(('主存档', SAVE_FILE))
    
    for i in range(1, MAX_BACKUPS + 1):
        backup_path = get_backup_path(i)
        if os.path.exists(backup_path):
            found_saves.append((f'备份 #{i}', backup_path))
    
    if not found_saves:
        print_color("  没有找到任何存档文件。", 'yellow')
        print(color_text("=" * 50, 'cyan'))
        return
    
    for name, path in found_saves:
        print(f"\n  [{name}]")
        print_color(f"  路径: {path}", 'white')
        
        try:
            file_size = os.path.getsize(path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(path))
            print_color(f"  大小: {file_size} 字节", 'cyan')
            print_color(f"  修改时间: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}", 'cyan')
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            is_valid, msg = validate_save_data(data)
            if is_valid:
                player_data = data.get('player', {})
                print_color(f"  状态: 有效", 'green')
                print_color(f"  角色: {player_data.get('name', '未知')}", 'green')
                print_color(f"  等级: {player_data.get('level', 1)}", 'green')
                print_color(f"  金币: {player_data.get('gold', 0)}", 'green')
                print_color(f"  位置: {player_data.get('current_location', '未知')}", 'green')
            else:
                print_color(f"  状态: 无效 ({msg})", 'red')
                
        except json.JSONDecodeError:
            print_color(f"  状态: 损坏 (JSON格式错误)", 'red')
        except Exception as e:
            print_color(f"  读取错误: {e}", 'red')
    
    print("\n" + color_text("=" * 50, 'cyan'))
