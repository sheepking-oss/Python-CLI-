from colors import print_color, color_text, print_quest

def show_quests(player):
    print("\n" + color_text("=" * 50, 'cyan'))
    print(color_text("  任务列表", 'bold'))
    print(color_text("=" * 50, 'cyan'))
    
    incomplete_quests = player.get_incomplete_quests()
    completed_quests = player.get_completed_quests()
    
    if incomplete_quests:
        print_color("\n  进行中的任务:", 'yellow')
        for quest in incomplete_quests:
            print_quest(quest)
    
    if completed_quests:
        print_color("\n  已完成的任务:", 'green')
        for quest in completed_quests:
            print_quest(quest, show_progress=False)
    
    if not incomplete_quests and not completed_quests:
        print_color("  没有可用的任务。", 'yellow')
    
    print(color_text("=" * 50, 'cyan'))
    
    if completed_quests:
        print_color("\n  [C] 领取已完成任务的奖励", 'yellow')
    
    print_color("  [0] 返回", 'yellow')
    
    choice = input("\n  选择: ").strip().upper()
    
    if choice == 'C' and completed_quests:
        claim_rewards(player)
    
    return

def claim_rewards(player):
    completed_quests = player.get_completed_quests()
    
    if not completed_quests:
        print_color("  没有可领取奖励的任务。", 'yellow')
        return
    
    total_gold = 0
    total_exp = 0
    
    quests_to_claim = [q['id'] for q in completed_quests]
    
    for quest_id in quests_to_claim:
        for quest in player.quests:
            if quest['id'] == quest_id and quest['completed']:
                total_gold += quest['gold_reward']
                total_exp += quest['exp_reward']
                player.quests.remove(quest)
                break
    
    player.gain_gold(total_gold)
    leveled_up = player.gain_exp(total_exp)
    
    print_color(f"\n  领取奖励成功！", 'green')
    print_color(f"  获得 {total_gold} 金币和 {total_exp} 经验值！", 'yellow')
    
    if leveled_up:
        print_color(f"\n  恭喜！你升级到了 {player.level} 级！", 'cyan')

def show_quest_progress(player):
    print("\n" + color_text("=" * 50, 'cyan'))
    print(color_text("  任务进度", 'bold'))
    print(color_text("=" * 50, 'cyan'))
    
    for quest in player.quests:
        if not quest['completed']:
            print_quest(quest)
        else:
            print_color(f"\n  [已完成] {quest['name']} - 按 C 领取奖励", 'green')
    
    print(color_text("=" * 50, 'cyan'))
