import random
import time
import sys
import os
from typing import Dict, List, Optional

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text: str, delay: float = 0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class Item:
    def __init__(self, name: str, description: str, value: int = 0, damage: int = 0):
        self.name = name
        self.description = description
        self.value = value
        self.damage = damage

class Enemy:
    def __init__(self, name: str, health: int, damage: int, loot: List[str]):
        self.name = name
        self.health = health
        self.damage = damage
        self.loot = loot

class Player:
    def __init__(self):
        self.health = 100
        self.max_health = 100
        self.gold = 0
        self.inventory: List[str] = []
        self.current_location = "dock"
        self.has_map = False
        self.has_key = False
        self.level = 1
        self.experience = 0
        self.experience_to_level = 100
        self.base_damage = 10
        self.equipped_weapon: Optional[str] = None

    def level_up(self):
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.base_damage += 5
        self.experience_to_level = int(self.experience_to_level * 1.5)
        return f"{Colors.GREEN}Level Up! You are now level {self.level}!{Colors.ENDC}"

    def gain_experience(self, amount: int):
        self.experience += amount
        if self.experience >= self.experience_to_level:
            self.experience -= self.experience_to_level
            return self.level_up()
        return ""

    def get_total_damage(self) -> int:
        weapon_damage = 0
        if self.equipped_weapon == "rusty_sword":
            weapon_damage = 5
        elif self.equipped_weapon == "steel_sword":
            weapon_damage = 10
        elif self.equipped_weapon == "magic_cutlass":
            weapon_damage = 20
        return self.base_damage + weapon_damage

class Game:
    def __init__(self):
        self.player = Player()
        self.game_running = True
        self.quest_log: List[str] = []
        self.enemies = self._initialize_enemies()
        self.items = self._initialize_items()

    def _initialize_enemies(self) -> Dict[str, Enemy]:
        return {
            "rookie_pirate": Enemy("Rookie Pirate", 30, 5, ["rusty_sword", "small_potion"]),
            "seasoned_pirate": Enemy("Seasoned Pirate", 50, 10, ["steel_sword", "medium_potion"]),
            "pirate_captain": Enemy("Pirate Captain", 100, 15, ["magic_cutlass", "large_potion", "treasure_map"]),
            "ghost_pirate": Enemy("Ghost Pirate", 80, 20, ["spectral_key", "ghost_essence"]),
            "kraken_spawn": Enemy("Kraken Spawn", 120, 25, ["kraken_tentacle", "ocean_pearl"])
        }

    def _initialize_items(self) -> Dict[str, Item]:
        return {
            "rusty_sword": Item("Rusty Sword", "An old but serviceable blade", 10, 5),
            "steel_sword": Item("Steel Sword", "A well-crafted weapon", 50, 10),
            "magic_cutlass": Item("Magic Cutlass", "A powerful enchanted blade", 200, 20),
            "small_potion": Item("Small Health Potion", "Restores 20 HP", 10),
            "medium_potion": Item("Medium Health Potion", "Restores 50 HP", 25),
            "large_potion": Item("Large Health Potion", "Restores 100 HP", 50),
            "compass": Item("Golden Compass", "Points to mysterious locations", 100),
            "treasure_map": Item("Ancient Map", "Shows the way to great treasure", 150),
            "spectral_key": Item("Spectral Key", "Opens supernatural locks", 300),
            "ghost_essence": Item("Ghost Essence", "Mysterious ethereal substance", 200),
            "kraken_tentacle": Item("Kraken Tentacle", "A powerful magical ingredient", 400),
            "ocean_pearl": Item("Ocean Pearl", "A rare and valuable gem", 500)
        }
        
    ASCII_ART = {
        "ship": r"""
          |    |    |
         )_)  )_)  )_)
        )___))___))___)\
       )____)____)_____)\
     _____|____|____|____\__
     \                   /
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""",
        
        "treasure": r"""
           _.--.
       _.-'_:-'||
   _.-'_.-::::'||
._-:'_.-::::::'  ||
.'`-.-:::::::'   ||
/.'`;|:::::::'    ||_
||   ||::::::'    _.;._'-._
||   ||:::::'  .-'    `    `-.
||   ||:::::' /          `-.  `-._
||   ||:::::' |       _____  `-.   `-.
||   ||:::::' |    .'     `-.  `-.    `-.
||   ||:::::' |   /          `-.  `-.    `-.""",
        
        "sword": r"""
     /\
    /  \
    |  |
    |  |
    |  |
    |  |
    |  |
  --+--+--
    |  |
    |  |
    \  /
     \/""",
        
        "skull": r"""
     _______________
    /               \
   /                 \
  /                   \
 |   XXXX     XXXX   |
 |   XXXX     XXXX   |
 |   XXX       XXX   |
 |         X         |
 \__      XXX     __/
   |\     XXX     /|
   | |           | |
   | I I I I I I I |
   |  I I I I I I  |
    \_           _/
      \_________/"""
    }
    
    LOCATIONS = {
        "dock": {
            "description": "A bustling port filled with ships and sailors. The salty air fills your lungs.",
            "connections": ["tavern", "market", "ship"],
            "items": ["compass", "rusty_sword"],
            "enemies": ["rookie_pirate"]
        },
        "tavern": {
            "description": "A dimly lit tavern where pirates share tales of treasure and adventure.",
            "connections": ["dock", "secret_room"],
            "items": ["small_potion"],
            "enemies": ["seasoned_pirate"]
        },
        "market": {
            "description": "A crowded marketplace with vendors selling exotic goods from distant lands.",
            "connections": ["dock", "alley", "blacksmith"],
            "items": ["medium_potion"],
            "enemies": []
        },
        "ship": {
            "description": "Your trusty vessel, ready to sail the seven seas in search of adventure.",
            "connections": ["dock", "island", "mysterious_fog"],
            "items": [],
            "enemies": []
        },
        "island": {
            "description": "A mysterious island shrouded in legends of buried treasure.",
            "connections": ["ship", "cave", "jungle"],
            "items": ["treasure_map"],
            "enemies": ["ghost_pirate"]
        },
        "cave": {
            "description": "A dark cave with ancient markings and the echoes of the ocean.",
            "connections": ["island", "treasure_room"],
            "items": ["spectral_key"],
            "enemies": ["pirate_captain"]
        },
        "alley": {
            "description": "A dangerous back alley where cutthroats and thieves lurk in shadows.",
            "connections": ["market"],
            "items": ["steel_sword"],
            "enemies": ["seasoned_pirate"]
        },
        "blacksmith": {
            "description": "A forge where master craftsmen create powerful weapons.",
            "connections": ["market"],
            "items": [],
            "enemies": []
        },
        "secret_room": {
            "description": "A hidden chamber accessible only to those who know its existence.",
            "connections": ["tavern"],
            "items": ["magic_cutlass"],
            "enemies": []
        },
        "mysterious_fog": {
            "description": "A supernatural fog bank hiding unknown dangers.",
            "connections": ["ship", "ghost_ship"],
            "items": [],
            "enemies": ["ghost_pirate"]
        },
        "ghost_ship": {
            "description": "An ethereal vessel crewed by supernatural beings.",
            "connections": ["mysterious_fog"],
            "items": ["ghost_essence"],
            "enemies": ["ghost_pirate"]
        },
        "jungle": {
            "description": "A dense tropical forest hiding ancient secrets.",
            "connections": ["island", "temple_ruins"],
            "items": ["large_potion"],
            "enemies": ["kraken_spawn"]
        },
        "temple_ruins": {
            "description": "The remains of an ancient civilization's sacred place.",
            "connections": ["jungle"],
            "items": ["ocean_pearl"],
            "enemies": ["pirate_captain"]
        },
        "treasure_room": {
            "description": "A grand chamber filled with unimaginable riches.",
            "connections": ["cave"],
            "items": ["treasure"],
            "enemies": []
        }
    }

    def display_status_bar(self):
        health_percentage = (self.player.health / self.player.max_health) * 20
        health_bar = "█" * int(health_percentage) + "░" * (20 - int(health_percentage))
        exp_percentage = (self.player.experience / self.player.experience_to_level) * 20
        exp_bar = "█" * int(exp_percentage) + "░" * (20 - int(exp_percentage))
        
        print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}Level: {self.player.level} | Gold: {self.player.gold}{Colors.ENDC}")
        print(f"{Colors.RED}Health: [{health_bar}] {self.player.health}/{self.player.max_health}{Colors.ENDC}")
        print(f"{Colors.BLUE}EXP:    [{exp_bar}] {self.player.experience}/{self.player.experience_to_level}{Colors.ENDC}")
        print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

    def display_location(self):
        clear_screen()
        self.display_status_bar()
        location = self.LOCATIONS[self.player.current_location]
        
        print(f"{Colors.BOLD}{Colors.YELLOW}Location: {self.player.current_location.upper()}{Colors.ENDC}")
        print_slow(f"{Colors.BLUE}{location['description']}{Colors.ENDC}")
        
        if self.player.current_location in self.ASCII_ART:
            print(f"{Colors.GREEN}{self.ASCII_ART[self.player.current_location]}{Colors.ENDC}")
            
        print(f"\n{Colors.YELLOW}Paths:{Colors.ENDC} {', '.join(location['connections'])}")
        if location['items']:
            print(f"{Colors.GREEN}Items here:{Colors.ENDC} {', '.join(location['items'])}")
        if self.player.inventory:
            print(f"{Colors.BLUE}Inventory:{Colors.ENDC} {', '.join(self.player.inventory)}")
        if self.quest_log:
            print(f"\n{Colors.YELLOW}Active Quests:{Colors.ENDC}")
            for quest in self.quest_log:
                print(f"- {quest}")

    def handle_combat(self, enemy_type: str):
        enemy = self.enemies[enemy_type]
        enemy_current_health = enemy.health
        print(f"\n{Colors.RED}A {enemy.name} appears!{Colors.ENDC}")
        print(self.ASCII_ART["skull"])
        
        while enemy_current_health > 0 and self.player.health > 0:
            print(f"\n{Colors.RED}Enemy Health: {enemy_current_health}/{enemy.health}{Colors.ENDC}")
            action = input(f"\n{Colors.YELLOW}What do you do? (attack/use_potion/run):{Colors.ENDC} ").lower()
            
            if action == "attack":
                damage = self.player.get_total_damage()
                enemy_current_health -= damage
                print(f"\n{Colors.GREEN}You dealt {damage} damage to the {enemy.name}!{Colors.ENDC}")
                
                if enemy_current_health > 0:
                    player_damage = enemy.damage
                    self.player.health -= player_damage
                    print(f"{Colors.RED}The {enemy.name} hit you for {player_damage} damage!{Colors.ENDC}")
                    
            elif action == "use_potion":
                potions = [item for item in self.player.inventory if "potion" in item]
                if not potions:
                    print(f"{Colors.RED}You don't have any potions!{Colors.ENDC}")
                    continue
                    
                print(f"\n{Colors.GREEN}Available potions:{Colors.ENDC}")
                for i, potion in enumerate(potions, 1):
                    print(f"{i}. {potion}")
                    
                try:
                    choice = int(input("Choose a potion (number): ")) - 1
                    if 0 <= choice < len(potions):
                        potion = potions[choice]
                        self.use_potion(potion)
                    else:
                        print(f"{Colors.RED}Invalid choice!{Colors.ENDC}")
                except ValueError:
                    print(f"{Colors.RED}Invalid input!{Colors.ENDC}")
                    
            elif action == "run":
                if random.random() < 0.4:
                    print(f"\n{Colors.GREEN}You successfully escaped!{Colors.ENDC}")
                    return True
                else:
                    print(f"\n{Colors.RED}You failed to escape!{Colors.ENDC}")
                    player_damage = enemy.damage
                    self.player.health -= player_damage
                    print(f"{Colors.RED}The {enemy.name} hit you for {player_damage} damage!{Colors.ENDC}")
            
            if enemy_current_health <= 0:
                print(f"\n{Colors.GREEN}You defeated the {enemy.name}!{Colors.ENDC}")
                exp_gain = random.randint(20, 50)
                level_up_message = self.player.gain_experience(exp_gain)
                print(f"{print(f"{Colors.GREEN}You gained {exp_gain} experience!{Colors.ENDC}")
                if level_up_message:
                    print(level_up_message)
                    
                # Handle loot
                gold_reward = random.randint(10, 30) * self.player.level
                self.player.gold += gold_reward
                print(f"{Colors.YELLOW}You found {gold_reward} gold!{Colors.ENDC}")
                
                # Drop random loot
                if enemy.loot and random.random() < 0.7:
                    dropped_item = random.choice(enemy.loot)
                    if dropped_item not in self.player.inventory:
                        self.player.inventory.append(dropped_item)
                        print(f"{Colors.GREEN}You found: {dropped_item}!{Colors.ENDC}")
                return False
            
        if self.player.health <= 0:
            print(f"\n{Colors.RED}You have been defeated...{Colors.ENDC}")
            self.game_running = False
            return False

    def use_potion(self, potion: str):
        healing = {
            "small_potion": 20,
            "medium_potion": 50,
            "large_potion": 100
        }
        
        if potion in healing:
            heal_amount = healing[potion]
            self.player.health = min(self.player.max_health, self.player.health + heal_amount)
            self.player.inventory.remove(potion)
            print(f"\n{Colors.GREEN}You used {potion} and recovered {heal_amount} health!{Colors.ENDC}")
        else:
            print(f"\n{Colors.RED}Invalid potion!{Colors.ENDC}")

    def shop_menu(self):
        if self.player.current_location != "market":
            return
            
        shop_items = {
            "small_potion": 15,
            "medium_potion": 30,
            "large_potion": 60,
            "steel_sword": 100
        }
        
        while True:
            clear_screen()
            print(f"\n{Colors.YELLOW}{'='*20} SHOP {'='*20}{Colors.ENDC}")
            print(f"{Colors.YELLOW}Your gold: {self.player.gold}{Colors.ENDC}")
            print("\nAvailable items:")
            
            for item, price in shop_items.items():
                print(f"{Colors.GREEN}{item}{Colors.ENDC}: {price} gold")
                
            print(f"\n{Colors.BLUE}Enter item name to buy or 'exit' to leave shop{Colors.ENDC}")
            choice = input(">>> ").lower()
            
            if choice == "exit":
                break
                
            if choice in shop_items:
                if self.player.gold >= shop_items[choice]:
                    self.player.gold -= shop_items[choice]
                    self.player.inventory.append(choice)
                    print(f"\n{Colors.GREEN}Purchased {choice}!{Colors.ENDC}")
                else:
                    print(f"\n{Colors.RED}Not enough gold!{Colors.ENDC}")
            else:
                print(f"\n{Colors.RED}Invalid item!{Colors.ENDC}")
            
            time.sleep(1)

    def handle_quests(self):
        location = self.player.current_location
        
        # Add new quests based on location and inventory
        if location == "tavern" and "Find the ghost ship" not in self.quest_log:
            self.quest_log.append("Find the ghost ship")
            print(f"\n{Colors.YELLOW}New Quest: Find the ghost ship{Colors.ENDC}")
            
        elif location == "island" and "Explore the temple ruins" not in self.quest_log:
            self.quest_log.append("Explore the temple ruins")
            print(f"\n{Colors.YELLOW}New Quest: Explore the temple ruins{Colors.ENDC}")
            
        # Complete quests
        if location == "ghost_ship" and "Find the ghost ship" in self.quest_log:
            self.quest_log.remove("Find the ghost ship")
            self.player.gold += 200
            print(f"\n{Colors.GREEN}Quest completed: Find the ghost ship{Colors.ENDC}")
            print(f"{Colors.YELLOW}Reward: 200 gold{Colors.ENDC}")
            
        elif location == "temple_ruins" and "Explore the temple ruins" in self.quest_log:
            self.quest_log.remove("Explore the temple ruins")
            self.player.gold += 300
            print(f"\n{Colors.GREEN}Quest completed: Explore the temple ruins{Colors.ENDC}")
            print(f"{Colors.YELLOW}Reward: 300 gold{Colors.ENDC}")

    def handle_input(self):
        print(f"\n{Colors.YELLOW}What would you like to do?{Colors.ENDC}")
        print("1. Move")
        print("2. Take item")
        print("3. Use item")
        print("4. View inventory")
        print("5. Shop (if in market)")
        print("6. Quit")
        
        choice = input(f"\n{Colors.GREEN}Choose an action (1-6):{Colors.ENDC} ")
        
        if choice == "1":
            print(f"\n{Colors.YELLOW}Where would you like to go?{Colors.ENDC}")
            print(f"Available locations: {', '.join(self.LOCATIONS[self.player.current_location]['connections'])}")
            new_location = input(f"\n{Colors.GREEN}Enter location:{Colors.ENDC} ").lower()
            
            if new_location in self.LOCATIONS[self.player.current_location]["connections"]:
                if new_location == "island" and "compass" not in self.player.inventory:
                    print(f"\n{Colors.RED}You need a compass to navigate to the island!{Colors.ENDC}")
                    time.sleep(2)
                    return
                if new_location == "cave" and not self.player.has_map:
                    print(f"\n{Colors.RED}You need a map to find the cave entrance!{Colors.ENDC}")
                    time.sleep(2)
                    return
                if new_location == "treasure_room" and not self.player.has_key:
                    print(f"\n{Colors.RED}You need the spectral key to enter the treasure room!{Colors.ENDC}")
                    time.sleep(2)
                    return
                    
                self.player.current_location = new_location
                self.handle_quests()
                
                # Handle random encounters
                if random.random() < 0.3 and self.LOCATIONS[new_location]["enemies"]:
                    enemy_type = random.choice(self.LOCATIONS[new_location]["enemies"])
                    self.handle_combat(enemy_type)
            else:
                print(f"\n{Colors.RED}You can't go there from here!{Colors.ENDC}")
                time.sleep(1)
                
        elif choice == "2":
            location = self.LOCATIONS[self.player.current_location]
            if not location["items"]:
                print(f"\n{Colors.RED}Nothing to take here!{Colors.ENDC}")
                time.sleep(1)
                return
                
            print(f"\n{Colors.YELLOW}What would you like to take?{Colors.ENDC}")
            print(f"Available items: {', '.join(location['items'])}")
            item = input(f"\n{Colors.GREEN}Enter item name:{Colors.ENDC} ").lower()
            
            if item in location["items"]:
                if item == "treasure" and not self.player.has_key:
                    print(f"\n{Colors.RED}You need the spectral key to get the treasure!{Colors.ENDC}")
                    time.sleep(2)
                    return
                    
                self.player.inventory.append(item)
                location["items"].remove(item)
                
                if item == "treasure_map":
                    self.player.has_map = True
                elif item == "spectral_key":
                    self.player.has_key = True
                elif item == "treasure":
                    self.player.gold += 1000
                    print(f"\n{Colors.GREEN}Congratulations! You found the treasure!{Colors.ENDC}")
                    print(f"{Colors.YELLOW}You gained 1000 gold!{Colors.ENDC}")
                    time.sleep(2)
                    
                print(f"\n{Colors.GREEN}You picked up: {item}{Colors.ENDC}")
                time.sleep(1)
            else:
                print(f"\n{Colors.RED}That item isn't here!{Colors.ENDC}")
                time.sleep(1)
                
        elif choice == "3":
            if not self.player.inventory:
                print(f"\n{Colors.RED}Your inventory is empty!{Colors.ENDC}")
                time.sleep(1)
                return
                
            print(f"\n{Colors.YELLOW}Choose an item to use:{Colors.ENDC}")
            for i, item in enumerate(self.player.inventory, 1):
                print(f"{i}. {item}")
                
            try:
                item_choice = int(input(f"\n{Colors.GREEN}Enter item number:{Colors.ENDC} ")) - 1
                if 0 <= item_choice < len(self.player.inventory):
                    item = self.player.inventory[item_choice]
                    if "potion" in item:
                        self.use_potion(item)
                    elif "_sword" in item:
                        self.player.equipped_weapon = item
                        print(f"\n{Colors.GREEN}Equipped {item}!{Colors.ENDC}")
                    else:
                        print(f"\n{Colors.RED}Can't use that item right now!{Colors.ENDC}")
                else:
                    print(f"\n{Colors.RED}Invalid choice!{Colors.ENDC}")
            except ValueError:
                print(f"\n{Colors.RED}Invalid input!{Colors.ENDC}")
                
        elif choice == "4":
            print(f"\n{Colors.YELLOW}Your inventory:{Colors.ENDC}")
            if self.player.inventory:
                for item in self.player.inventory:
                    print(f"- {item}")
            else:
                print("Empty")
            input(f"\n{Colors.GREEN}Press Enter to continue...{Colors.ENDC}")
            
        elif choice == "5":
            self.shop_menu()
            
        elif choice == "6":
            self.game_running = False
            
    def run(self):
        print_slow(f"""{Colors.YELLOW}
Welcome to Pirate Adventure!
Find the legendary treasure, but beware of dangerous pirates!
You'll need various items to succeed in your quest.
{Colors.ENDC}""")
        input(f"{Colors.GREEN}Press Enter to start...{Colors.ENDC}")
        
        while self.game_running and self.player.health > 0:
            self.display_location()
            self.handle_input()
            
        if self.player.health <= 0:
            print(f"\n{Colors.RED}Game Over! You died!{Colors.ENDC}")
        else:
            print(f"\n{Colors.GREEN}Thanks for playing!{Colors.ENDC}")
            if "treasure" in self.player.inventory:
                print(f"{Colors.YELLOW}Congratulations on finding the treasure!{Colors.ENDC}")
                print(f"Final gold count: {self.player.gold}")

if __name__ == "__main__":
    game = Game()
    game.run()
