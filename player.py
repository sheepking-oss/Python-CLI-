from config import QUESTS

class Player:
    def __init__(self, name="冒险者"):
        self.name = name
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.defense = 5
        self.gold = 50
        
        self.inventory = {}
        self.quests = [q.copy() for q in QUESTS]
        
        self.current_location = 'village'
        self.current_story_node = 'start'
        self.story_flags = {}
        
        self.total_gold_earned = 0
        self.monsters_killed = {}
        
        self.has_artifact = False
        self.defeated_dragon = False
        self.accepted_main_quest = False

    def gain_exp(self, amount):
        self.exp += amount
        leveled_up = False
        
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            self.exp_to_next = int(self.exp_to_next * 1.5)
            
            self.max_health += 20
            self.health = self.max_health
            self.attack += 3
            self.defense += 2
            
            leveled_up = True
        
        self._update_level_quests()
        return leveled_up

    def gain_gold(self, amount):
        self.gold += amount
        self.total_gold_earned += amount
        self._update_gold_quests()

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense // 2)
        self.health -= actual_damage
        return actual_damage

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def add_item(self, item_key, quantity=1):
        if item_key in self.inventory:
            self.inventory[item_key] += quantity
        else:
            self.inventory[item_key] = quantity

    def remove_item(self, item_key, quantity=1):
        if item_key in self.inventory:
            if self.inventory[item_key] >= quantity:
                self.inventory[item_key] -= quantity
                if self.inventory[item_key] == 0:
                    del self.inventory[item_key]
                return True
        return False

    def get_item_count(self, item_key):
        return self.inventory.get(item_key, 0)

    def has_item(self, item_key):
        return self.get_item_count(item_key) > 0

    def is_alive(self):
        return self.health > 0

    def kill_monster(self, monster_key):
        if monster_key in self.monsters_killed:
            self.monsters_killed[monster_key] += 1
        else:
            self.monsters_killed[monster_key] = 1
        
        self._update_kill_quests(monster_key)

    def _update_kill_quests(self, monster_key):
        for quest in self.quests:
            if not quest['completed'] and quest['type'] == 'kill' and quest['target'] == monster_key:
                quest['progress'] += 1
                if quest['progress'] >= quest['target_count']:
                    quest['completed'] = True

    def _update_gold_quests(self):
        for quest in self.quests:
            if not quest['completed'] and quest['type'] == 'gold':
                quest['progress'] = self.total_gold_earned
                if quest['progress'] >= quest['target']:
                    quest['completed'] = True

    def _update_level_quests(self):
        for quest in self.quests:
            if not quest['completed'] and quest['type'] == 'level':
                quest['progress'] = self.level
                if quest['progress'] >= quest['target']:
                    quest['completed'] = True

    def get_completed_quests(self):
        return [q for q in self.quests if q['completed']]

    def get_incomplete_quests(self):
        return [q for q in self.quests if not q['completed']]

    def claim_quest_reward(self, quest_id):
        for quest in self.quests:
            if quest['id'] == quest_id and quest['completed']:
                self.gain_gold(quest['gold_reward'])
                self.gain_exp(quest['exp_reward'])
                self.quests.remove(quest)
                return True
        return False

    def set_flag(self, flag_name, value=True):
        self.story_flags[flag_name] = value
        
        if flag_name == 'has_artifact':
            self.has_artifact = value
            if value:
                self.attack += 20
                self.defense += 10
        elif flag_name == 'defeated_dragon':
            self.defeated_dragon = value
        elif flag_name == 'accepted_main_quest':
            self.accepted_main_quest = value

    def has_flag(self, flag_name):
        return self.story_flags.get(flag_name, False)

    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'exp': self.exp,
            'exp_to_next': self.exp_to_next,
            'health': self.health,
            'max_health': self.max_health,
            'attack': self.attack,
            'defense': self.defense,
            'gold': self.gold,
            'inventory': self.inventory,
            'quests': self.quests,
            'current_location': self.current_location,
            'current_story_node': self.current_story_node,
            'story_flags': self.story_flags,
            'total_gold_earned': self.total_gold_earned,
            'monsters_killed': self.monsters_killed,
            'has_artifact': self.has_artifact,
            'defeated_dragon': self.defeated_dragon,
            'accepted_main_quest': self.accepted_main_quest
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data.get('name', '冒险者'))
        
        player.level = data.get('level', 1)
        player.exp = data.get('exp', 0)
        player.exp_to_next = data.get('exp_to_next', 100)
        player.health = data.get('health', 100)
        player.max_health = data.get('max_health', 100)
        player.attack = data.get('attack', 10)
        player.defense = data.get('defense', 5)
        player.gold = data.get('gold', 50)
        player.inventory = data.get('inventory', {})
        player.quests = data.get('quests', [q.copy() for q in QUESTS])
        player.current_location = data.get('current_location', 'village')
        player.current_story_node = data.get('current_story_node', 'start')
        player.story_flags = data.get('story_flags', {})
        player.total_gold_earned = data.get('total_gold_earned', 0)
        player.monsters_killed = data.get('monsters_killed', {})
        player.has_artifact = data.get('has_artifact', False)
        player.defeated_dragon = data.get('defeated_dragon', False)
        player.accepted_main_quest = data.get('accepted_main_quest', False)
        
        return player
