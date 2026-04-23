import os

SAVE_DIR = os.path.join(os.path.dirname(__file__), 'saves')
SAVE_FILE = os.path.join(SAVE_DIR, 'game_save.json')

COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
    'bg_blue': '\033[44m',
}

ITEMS = {
    'health_potion': {
        'name': '生命药水',
        'description': '恢复 50 点生命值',
        'price': 30,
        'type': 'consumable',
        'effect': {'health': 50}
    },
    'large_health_potion': {
        'name': '大型生命药水',
        'description': '恢复 100 点生命值',
        'price': 60,
        'type': 'consumable',
        'effect': {'health': 100}
    },
    'attack_boost': {
        'name': '力量药剂',
        'description': '永久增加 5 点攻击力',
        'price': 100,
        'type': 'permanent',
        'effect': {'attack': 5}
    },
    'defense_boost': {
        'name': '坚韧药剂',
        'description': '永久增加 3 点防御力',
        'price': 80,
        'type': 'permanent',
        'effect': {'defense': 3}
    },
    'magic_scroll': {
        'name': '魔法卷轴',
        'description': '对敌人造成 80 点伤害',
        'price': 50,
        'type': 'combat',
        'effect': {'damage': 80}
    }
}

MONSTERS = {
    'slime': {
        'name': '史莱姆',
        'health': 30,
        'attack': 5,
        'defense': 2,
        'gold_reward': 10,
        'exp_reward': 15,
        'description': '一个普通的史莱姆'
    },
    'goblin': {
        'name': '哥布林',
        'health': 50,
        'attack': 10,
        'defense': 5,
        'gold_reward': 20,
        'exp_reward': 25,
        'description': '一个狡猾的哥布林'
    },
    'wolf': {
        'name': '野狼',
        'health': 60,
        'attack': 15,
        'defense': 4,
        'gold_reward': 25,
        'exp_reward': 30,
        'description': '一只凶猛的野狼'
    },
    'orc': {
        'name': '兽人',
        'health': 80,
        'attack': 18,
        'defense': 8,
        'gold_reward': 35,
        'exp_reward': 40,
        'description': '一个强壮的兽人'
    },
    'skeleton': {
        'name': '骷髅战士',
        'health': 70,
        'attack': 20,
        'defense': 10,
        'gold_reward': 40,
        'exp_reward': 45,
        'description': '一个复活的骷髅战士'
    },
    'dragon': {
        'name': '幼龙',
        'health': 150,
        'attack': 30,
        'defense': 15,
        'gold_reward': 100,
        'exp_reward': 100,
        'description': '一只年幼但强大的龙'
    },
    'dark_lord': {
        'name': '黑暗领主',
        'health': 300,
        'attack': 40,
        'defense': 20,
        'gold_reward': 500,
        'exp_reward': 500,
        'description': '统治这片土地的邪恶存在'
    }
}

SHOP_ITEMS = ['health_potion', 'large_health_potion', 'attack_boost', 'defense_boost', 'magic_scroll']

QUESTS = [
    {
        'id': 'kill_slimes',
        'name': '消灭史莱姆',
        'description': '消灭 5 只史莱姆',
        'type': 'kill',
        'target': 'slime',
        'target_count': 5,
        'progress': 0,
        'gold_reward': 50,
        'exp_reward': 30,
        'completed': False
    },
    {
        'id': 'kill_goblins',
        'name': '哥布林猎手',
        'description': '消灭 3 只哥布林',
        'type': 'kill',
        'target': 'goblin',
        'target_count': 3,
        'progress': 0,
        'gold_reward': 80,
        'exp_reward': 50,
        'completed': False
    },
    {
        'id': 'collect_gold',
        'name': '财富积累',
        'description': '累计获得 200 金币',
        'type': 'gold',
        'target': 200,
        'progress': 0,
        'gold_reward': 100,
        'exp_reward': 60,
        'completed': False
    },
    {
        'id': 'reach_level_5',
        'name': '成长之路',
        'description': '达到 5 级',
        'type': 'level',
        'target': 5,
        'progress': 0,
        'gold_reward': 150,
        'exp_reward': 100,
        'completed': False
    }
]

MAP_LOCATIONS = {
    'village': {
        'name': '宁静村',
        'description': '一个和平的小村庄，是你冒险的起点。',
        'encounter_chance': 0,
        'connected': ['forest', 'shop'],
        'has_shop': True
    },
    'forest': {
        'name': '迷雾森林',
        'description': '充满神秘生物的森林，小心前行。',
        'encounter_chance': 0.4,
        'monsters': ['slime', 'goblin', 'wolf'],
        'connected': ['village', 'mountain', 'cave'],
        'has_shop': False
    },
    'mountain': {
        'name': '险峻山脉',
        'description': '高耸入云的山脉，危险但也有珍贵的宝物。',
        'encounter_chance': 0.5,
        'monsters': ['orc', 'skeleton', 'wolf'],
        'connected': ['forest', 'dragon_lair'],
        'has_shop': False
    },
    'cave': {
        'name': '黑暗洞穴',
        'description': '深邃的洞穴，似乎有什么在等待着你。',
        'encounter_chance': 0.6,
        'monsters': ['skeleton', 'orc'],
        'connected': ['forest', 'dark_lord_castle'],
        'has_shop': False
    },
    'dragon_lair': {
        'name': '巨龙巢穴',
        'description': '传说中的巨龙居住之地，只有勇者才能挑战。',
        'encounter_chance': 0.3,
        'monsters': ['dragon'],
        'connected': ['mountain'],
        'has_shop': False,
        'boss_area': True
    },
    'dark_lord_castle': {
        'name': '黑暗领主城堡',
        'description': '邪恶势力的大本营，最终的挑战在此等待。',
        'encounter_chance': 0.2,
        'monsters': ['skeleton', 'orc'],
        'connected': ['cave'],
        'has_shop': False,
        'final_boss': True
    },
    'shop': {
        'name': '村庄商店',
        'description': '可以购买各种道具的地方。',
        'encounter_chance': 0,
        'connected': ['village'],
        'has_shop': True
    }
}

STORY_NODES = {
    'start': {
        'text': '你醒来发现自己躺在一片草地上，记忆模糊不清。只记得自己是一名冒险者，被派来调查这片土地上出现的异常现象。',
        'choices': [
            {'text': '前往宁静村打听消息', 'next': 'village_entrance'},
            {'text': '直接进入迷雾森林探索', 'next': 'forest_entrance'}
        ]
    },
    'village_entrance': {
        'text': '你来到了宁静村的入口。村庄看起来很平静，但村民们的脸上都带着忧虑的神色。一位老者向你走来。',
        'choices': [
            {'text': '与老者交谈', 'next': 'talk_to_elder'},
            {'text': '直接前往商店', 'next': 'go_to_shop'},
            {'text': '离开村庄，前往森林', 'next': 'forest_entrance'}
        ]
    },
    'talk_to_elder': {
        'text': '"冒险者啊，感谢你来到这里。" 老者说道，"最近这片土地上出现了许多异常的生物，迷雾森林里的怪物也变得更加凶猛。据说这一切都与传说中的黑暗领主有关。你愿意帮助我们调查吗？"',
        'choices': [
            {'text': '接受老者的请求，承诺会调查清楚', 'next': 'accept_quest', 'reward': {'gold': 50}},
            {'text': '表示需要先了解更多情况', 'next': 'ask_more'},
            {'text': '拒绝，说自己只是路过', 'next': 'refuse_elder'}
        ]
    },
    'accept_quest': {
        'text': '"太好了！" 老者感激地说道，"这里有一些金币作为启动资金。请务必小心，黑暗领主的力量正在不断增长。你可以先去森林调查，或者去山脉寻找传说中的巨龙，它可能知道黑暗领主的弱点。"',
        'choices': [
            {'text': '前往迷雾森林', 'next': 'forest_entrance'},
            {'text': '前往险峻山脉', 'next': 'mountain_entrance'},
            {'text': '先去商店补给', 'next': 'go_to_shop'}
        ],
        'flag': 'accepted_main_quest'
    },
    'ask_more': {
        'text': '"当然，冒险者。" 老者说道，"黑暗领主曾经是一位强大的魔法师，但他追求禁忌的力量，最终堕落。他现在居住在黑暗洞穴深处的城堡里。要击败他，你需要足够的力量，或者找到传说中的神器。"',
        'choices': [
            {'text': '接受任务，帮助村民', 'next': 'accept_quest', 'reward': {'gold': 50}},
            {'text': '先去商店准备一下', 'next': 'go_to_shop'}
        ]
    },
    'refuse_elder': {
        'text': '"唉..." 老者失望地摇了摇头，转身离开了。你感到一丝愧疚，但还是决定继续自己的冒险。',
        'choices': [
            {'text': '前往迷雾森林', 'next': 'forest_entrance'},
            {'text': '改变主意，回去找老者', 'next': 'talk_to_elder'}
        ],
        'flag': 'refused_elder'
    },
    'go_to_shop': {
        'text': '你来到了村庄商店，店主热情地招待了你。',
        'choices': [
            {'text': '进入商店浏览商品', 'next': 'enter_shop'},
            {'text': '离开商店', 'next': 'village_entrance'}
        ]
    },
    'enter_shop': {
        'text': '商店里摆满了各种道具。',
        'choices': [],
        'action': 'open_shop'
    },
    'forest_entrance': {
        'text': '你站在迷雾森林的入口。森林里弥漫着一层薄薄的雾气，不时传来奇怪的声音。',
        'choices': [
            {'text': '深入森林探索', 'next': 'forest_explore'},
            {'text': '返回村庄', 'next': 'village_entrance'}
        ]
    },
    'forest_explore': {
        'text': '你在森林中小心翼翼地前进着...',
        'choices': [],
        'action': 'explore_forest'
    },
    'mountain_entrance': {
        'text': '你来到了险峻山脉的脚下。高耸的山峰直插云霄，山路崎岖难行。',
        'choices': [
            {'text': '开始攀登山脉', 'next': 'mountain_climb'},
            {'text': '返回森林', 'next': 'forest_entrance'}
        ]
    },
    'mountain_climb': {
        'text': '你艰难地在山路上攀爬着...',
        'choices': [],
        'action': 'explore_mountain'
    },
    'found_artifact': {
        'text': '在战斗中，你意外发现了一件古老的神器！它散发着神秘的光芒，似乎蕴含着强大的力量。',
        'choices': [
            {'text': '获取神器', 'next': 'get_artifact', 'reward': {'attack': 20, 'defense': 10}},
            {'text': '继续冒险，稍后再来', 'next': 'continue_adventure'}
        ]
    },
    'get_artifact': {
        'text': '你拿起了神器，立刻感到一股强大的力量涌入体内！你的攻击力和防御力都得到了显著提升。',
        'choices': [
            {'text': '继续冒险', 'next': 'continue_adventure'}
        ],
        'flag': 'has_artifact'
    },
    'defeated_dragon': {
        'text': '巨龙在你的攻击下倒下了！它在临死前说道："冒险者...黑暗领主...他的力量来自...深渊...只有神器...才能真正伤害他..."',
        'choices': [
            {'text': '继续探索', 'next': 'continue_adventure'}
        ],
        'flag': 'defeated_dragon'
    },
    'final_confrontation': {
        'text': '你终于来到了黑暗领主的面前。他端坐在王座上，周身环绕着黑暗的能量。',
        'choices': [
            {'text': '直接挑战黑暗领主', 'next': 'fight_dark_lord'},
            {'text': '尝试与他谈判', 'next': 'negotiate_dark_lord'}
        ]
    },
    'fight_dark_lord': {
        'text': '"愚蠢的冒险者！" 黑暗领主站起身来，"你以为凭你的力量就能击败我吗？"',
        'choices': [],
        'action': 'boss_battle'
    },
    'negotiate_dark_lord': {
        'text': '"谈判？" 黑暗领主发出一阵刺耳的笑声，"有趣。告诉我，你想要什么？"',
        'choices': [
            {'text': '请求他放过这片土地', 'next': 'beg_for_mercy'},
            {'text': '提出合作，分享力量', 'next': 'propose_alliance'},
            {'text': '放弃谈判，准备战斗', 'next': 'fight_dark_lord'}
        ]
    },
    'beg_for_mercy': {
        'text': '"放过他们？" 黑暗领主冷笑道，"这片土地本来就应该属于我。不过...我可以给你一个选择。加入我，成为我的手下，我可以饶你不死。"',
        'choices': [
            {'text': '接受提议，加入黑暗势力', 'next': 'join_dark_lord'},
            {'text': '拒绝，准备战斗', 'next': 'fight_dark_lord'}
        ]
    },
    'propose_alliance': {
        'text': '"合作？" 黑暗领主似乎来了兴趣，"你有什么资格与我合作？"',
        'choices': [
            {'text': '展示神器，证明你的价值', 'next': 'show_artifact', 'requires_flag': 'has_artifact'},
            {'text': '承诺提供情报和帮助', 'next': 'offer_help'},
            {'text': '放弃，准备战斗', 'next': 'fight_dark_lord'}
        ]
    },
    'show_artifact': {
        'text': '黑暗领主看到神器后，眼中闪过一丝恐惧。"这...这不可能！你从哪里得到的？" 他的声音有些颤抖。',
        'choices': [
            {'text': '利用神器的力量发起攻击', 'next': 'artifact_attack'},
            {'text': '提出交易，用神器换取和平', 'next': 'artifact_trade'}
        ]
    },
    'artifact_attack': {
        'text': '你举起神器，一道耀眼的光芒射向黑暗领主。他发出一声凄厉的惨叫，身体开始消散。"不...这不可能..."',
        'choices': [],
        'ending': 'true_hero'
    },
    'artifact_trade': {
        'text': '"交易？" 黑暗领主犹豫了一下，"好吧...把神器给我，我就离开这片土地，不再回来。"',
        'choices': [
            {'text': '相信他，交出神器', 'next': 'give_artifact'},
            {'text': '不相信，发起攻击', 'next': 'artifact_attack'}
        ]
    },
    'give_artifact': {
        'text': '你交出了神器。黑暗领主拿到神器后，突然大笑起来："愚蠢的冒险者！现在神器是我的了！" 他获得了神器的力量，变得更加强大。',
        'choices': [],
        'action': 'final_boss_boosted'
    },
    'offer_help': {
        'text': '"你的帮助？" 黑暗领主轻蔑地说道，"我不需要你的帮助。弱者只有被支配的命运。" 他举起手，准备发起攻击。',
        'choices': [],
        'action': 'boss_battle'
    },
    'join_dark_lord': {
        'text': '"很好！" 黑暗领主满意地点点头，"从今天起，你就是我的黑暗骑士。这片土地将在我们的统治下颤抖！"',
        'choices': [],
        'ending': 'dark_knight'
    },
    'continue_adventure': {
        'text': '你决定继续你的冒险之旅。',
        'choices': [],
        'action': 'free_explore'
    }
}

ENDINGS = {
    'true_hero': {
        'title': '真正的英雄',
        'description': '你用神器的力量击败了黑暗领主，拯救了这片土地。村民们为你欢呼，将你视为传奇英雄。你的名字将被永远铭记。',
        'epilogue': '多年后，人们仍然传颂着你的故事。宁静村建立了一座纪念碑，上面刻着你的事迹。每年的这一天，村民们都会聚集在这里，纪念这位拯救了他们的英雄。'
    },
    'dark_knight': {
        'title': '黑暗骑士',
        'description': '你选择加入黑暗势力，成为了黑暗领主的左右手。在你们的统治下，这片土地陷入了永恒的黑暗。',
        'epilogue': '你成为了黑暗军队的统帅，率领着怪物大军征服了一个又一个城市。虽然你获得了强大的力量，但内心深处偶尔会闪过一丝疑惑：这真的是你想要的吗？'
    },
    'victorious_warrior': {
        'title': '胜利的战士',
        'description': '虽然没有神器的帮助，但你凭借着过人的勇气和实力，艰难地击败了黑暗领主。',
        'epilogue': '你成为了人们口中的传奇战士。虽然没有神器的加持，但你的故事激励着一代又一代的冒险者。你用行动证明了，真正的力量来自于内心的勇气。'
    },
    'fallen_hero': {
        'title': '陨落的英雄',
        'description': '你在与黑暗领主的战斗中倒下了...',
        'epilogue': '你的牺牲没有白费。在你之后，更多的冒险者站了出来，继续与黑暗势力抗争。你的名字成为了勇气的象征，激励着后来者继续前行。'
    }
}
