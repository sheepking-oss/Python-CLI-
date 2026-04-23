#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from colors import print_title, print_menu, print_color, color_text, print_stats
from player import Player
from save_system import save_game, load_game, has_save_file, show_save_info
from inventory import show_inventory
from quest_system import show_quests
from shop import open_shop
from story import run_story

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_player_name():
    print("\n" + color_text("=" * 50, 'cyan'))
    print_color("  创建角色", 'bold')
    print(color_text("=" * 50, 'cyan'))
    
    while True:
        name = input("\n  请输入你的角色名: ").strip()
        
        if name:
            print_color(f"\n  你好，{name}！冒险即将开始...", 'green')
            return name
        else:
            print_color("  角色名不能为空！", 'red')

def new_game():
    clear_screen()
    print_title()
    
    name = get_player_name()
    player = Player(name)
    
    print_color("\n  按回车键开始冒险...", 'yellow')
    input()
    
    run_story(player)
    
    return player

def continue_game(player):
    if not player:
        return
    
    while True:
        print("\n" + color_text("=" * 50, 'cyan'))
        print(color_text("  游戏菜单", 'bold'))
        print(color_text("=" * 50, 'cyan'))
        
        print_color("  [1] 继续剧情", 'yellow')
        print_color("  [2] 自由探索", 'yellow')
        print_color("  [3] 查看背包", 'yellow')
        print_color("  [4] 查看任务", 'yellow')
        print_color("  [5] 查看角色状态", 'yellow')
        print_color("  [6] 保存游戏", 'yellow')
        print_color("  [0] 返回主菜单", 'yellow')
        
        choice = input("\n  选择: ").strip()
        
        if choice == '0':
            return
        
        elif choice == '1':
            run_story(player)
            if not player.is_alive():
                return
        
        elif choice == '2':
            from story import free_explore_mode
            result = free_explore_mode(player)
            if result == 'game_over':
                return
        
        elif choice == '3':
            show_inventory(player)
        
        elif choice == '4':
            show_quests(player)
        
        elif choice == '5':
            print_stats(player)
        
        elif choice == '6':
            save_game(player)
        
        else:
            print_color("  无效的选择！", 'red')

def show_help():
    print("\n" + color_text("=" * 60, 'cyan'))
    print(color_text("  游戏说明", 'bold'))
    print(color_text("=" * 60, 'cyan'))
    
    help_text = """
  【游戏概述】
  这是一款文字冒险游戏，你将扮演一名冒险者，
  探索神秘的世界，与怪物战斗，完成任务，
  并最终决定这片土地的命运。

  【基本操作】
  • 输入数字选择菜单选项
  • 按回车键确认选择

  【角色属性】
  • 生命值: 你的生命，降到0时游戏结束
  • 攻击力: 战斗中造成伤害的能力
  • 防御力: 减少受到的伤害
  • 经验值: 战斗获得，用于升级
  • 金币: 购买道具和装备

  【战斗系统】
  • 普通攻击: 对敌人造成伤害
  • 使用道具: 使用背包中的战斗道具
  • 逃跑: 有几率逃离战斗（Boss战无法逃跑）

  【道具系统】
  • 消耗型: 使用后立即生效（如生命药水）
  • 永久型: 使用后永久提升属性
  • 战斗型: 只能在战斗中使用

  【任务系统】
  • 完成任务可获得金币和经验奖励
  • 任务完成后记得领取奖励

  【存档系统】
  • 游戏中随时可以保存进度
  • 主菜单可以读取存档

  【提示】
  • 在商店购买足够的生命药水
  • 升级可以恢复全部生命值
  • 探索不同的区域可能触发特殊剧情
  • 你的选择会影响最终结局
"""
    
    print(help_text)
    print(color_text("=" * 60, 'cyan'))
    input("\n  按回车键返回主菜单...")

def main():
    player = None
    
    while True:
        clear_screen()
        print_title()
        print_menu()
        
        choice = input("\n  选择: ").strip()
        
        if choice == '1':
            player = new_game()
        
        elif choice == '2':
            if has_save_file():
                show_save_info()
                confirm = input("\n  确定要读取存档吗？(y/n): ").strip().lower()
                if confirm == 'y':
                    player = load_game()
                    if player:
                        continue_game(player)
            else:
                print_color("\n  没有找到存档文件！", 'yellow')
                input("\n  按回车键继续...")
        
        elif choice == '3':
            show_help()
        
        elif choice == '4':
            print_color("\n  感谢游玩！再见！", 'cyan')
            sys.exit(0)
        
        else:
            print_color("\n  无效的选择！", 'red')
            input("\n  按回车键继续...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_color("\n\n  游戏已退出。", 'yellow')
    except Exception as e:
        print_color(f"\n  游戏发生错误: {e}", 'red')
        import traceback
        traceback.print_exc()
        input("\n  按回车键退出...")
