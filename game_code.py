
# coding: utf-8

# This is a character creator for a simple fight game based on the D20 system in the consol. Coded by Greg Wee

# In[ ]:


from random import randint
from time import sleep

#Here's the common error mesage that's going to show up when anything doesn't match during creation.
sorry  = "I'm sorry, I don't recognize that input. Please try again."

#defining the character that's going to be fighting
class Character(object):
    #these will be modified by the character creation process later.
    hp = 0
    attack = 0
    defense = 0
    damage = 4
    damage_rand = 0
    weapon = ""
    
    def __init__(self, name):
        self.name = name
    
    def swing_attack(self, target_ac):
        print("%s swings his %s at the enemy!" % (self.name, self.weapon))
        roll = hitcheck(self.attack, target_ac)
        return roll
    
    def swing_damage(self):
        roll = randint(1, self.damage_rand) + self.damage
        return roll
        

#Defining the character creation process.
def name():
    choice = input("What is your name? ")
    return choice

def archetype():
    global Player
    choice = input("""What kind of warrior are you, a well armored KNIGHT, a balanced FIGHTER, or a nimble DUELIST?
    Type KNIGHT, FIGHTER, or DUELIST: """)
    if choice.upper() == 'KNIGHT':
        Player.hp = 100
        Player.defense = 13
        return
    elif choice.upper() == 'FIGHTER':
        Player.hp = 70
        Player.defense = 16
        return
    elif choice.upper() == 'DUELIST':
        Player.hp = 50
        Player.defense = 19
        return
    else:
        print(sorry)
        archetype()
        
def weapon_choice():
    global Player
    choice = input("""And what kind of weapon do you weild? A hefty BATTLEAXE, a versatile LONGSWORD, or the pinpoint SHORTSWORD?
    Type BATTLEAXE, LONGSWORD, or SHORTSWORD: """)
    if choice.upper() == 'BATTLEAXE':
        Player.damage_rand = 12
        Player.attack = 6
        Player.weapon = 'battleaxe'
        return
    elif choice.upper() == 'LONGSWORD':
        Player.damage_rand = 8
        Player.attack = 9
        Player.weapon = 'longsword'
        return
    elif choice.upper() == 'SHORTSWORD':
        Player.damage_rand = 6
        Player.attack = 11
        Player.weapon = 'shortsword'
        return
    else:
        print(sorry)
        weapon_choice()
        
#start the character creation process
print("Welcome to the fight simulator. Let's get started.")
sleep(1)
Player = Character(name())
archetype()
weapon_choice()

print(Player.name, Player.swing_damage())


# Enemies are defined here.

# In[ ]:


from random import randint

def roll_xdy(x, y):
    total = 0
    for num in range(x):
        total += randint(1,y)
    return total

def hitcheck(attackmod, defAC):
    roll = randint(1,20) 
    print("Roll was a " + str(roll))
    if roll == 20:
        #print ("Critical Hit!")
        return "Critical Hit!"
    elif roll == 1:
        #print ("Critical Fail!")
        return "Critical Fail!"
    else:
        roll += attackmod
        #print ("Roll mod was a " + str(roll))
        if roll > defAC:
            #print ("Hit")
            return 'Hit'
        elif roll <= defAC:
            #print ("Miss")
            return 'Miss'
        else:
            print ("Error")
    
    
    

class Bear(object):
    basehp = 45
    baseAC = 12
    def __init__(self, name):
        self.name = name
    def bite(self, char_defense):
        attackval = randint(1,8) + 4
        x = hitcheck(5, char_defense)
        print ("The bear bites you! It's a " + str(x))
        return [x, attackval]
    def claw(self, char_defense):
        attackval = roll_xdy(2,6) + 2
        x = hitcheck(3, char_defense)
        print("The bear tries to rake its claws through you. It's a %s" % x)
        return [x, attackval]
    def attack_selector(self, char_defense):
        attacks = [self.bite, self.bite, self.claw]
        selector = randint(0, len(attacks)-1)
        choice = attacks[selector](char_defense)
        return choice
      
class Goblin(object):
    basehp = 34
    baseAC = 15
    def __init__(self, name):
        self.name = name
    def shortsword(self, char_defense):
        attackval = roll_xdy(1,6) + 3
        x = hitcheck(6, char_defense)
        print("The goblin swings his rusty blade. It's a %s" % x)
        return [x, attackval]
    def attack_selector(self, char_defense):
        attacks = [self.shortsword]
        selector = randint(0, len(attacks)-1)
        choice = attacks[selector](char_defense)
        return choice
    
class Lich(object):
    basehp = 60
    baseAC = 14
    def __init__(self, name):
        self.name = name
    def attack_selector(self, char_defense):
        attacks = [self.firebolt, self.frostbolt, self.lightning]
        global monster_hp
        if monster_hp < 20:
            attacks = [self.power_word_die]
        selector = randint(0, len(attacks)-1)
        choice = attacks[selector](char_defense)
        return choice
    def firebolt(self, char_defense):
        attackval = roll_xdy(1,10) + 5
        x = hitcheck(5, char_defense)
        print("The lich casts a firebolt right at you. It's a %s" % x)
        return [x, attackval]
    def frostbolt(self, char_defense):
        attackval = roll_xdy(1, 6) + 3
        x = hitcheck(3, char_defense)
        print("The lich sprays an icy wind at you. It's a %s" % x)
        return [x, attackval]
    def lightning(self, char_defense):
        attackval = roll_xdy(2,4) + 1
        x = hitcheck(7, char_defense)
        print("Lightning jumps from the lich's staff. It's a %s" % x)
        return [x, attackval]
    def power_word_die(self, char_defense):
        print("The lich murmers some strange incantations you can't hear. It's a Critical Hit!")
        return ['Hit', 1000]
        
#Creating a pool of available monsters to square off against.       
monster1 = Bear("Kuma")
monster2 = Goblin("goblin")
monster3 = Lich("Lich")
opponents_pool = [monster1, monster2, monster3]


# Here's where the fight scripting is going to occur.

# In[ ]:


#Let's randomly select a monster from the available pool
selector = randint(0, len(opponents_pool)-1)
enemy = opponents_pool[selector]
print("The fight begins! You face off against %s" % (enemy.name))

monster_hp = enemy.basehp
player_hp = Player.hp
flee = True
counter = 1

def player_round():
    #Player actions
    global player_hp, monster_hp, flee
    print("Player HP: %d      Monster HP: %d" % (player_hp, monster_hp))
    sleep(0.5)
    player_choice = input(Player.name + " what do you want to do? ATTACK or FLEE ")
    sleep(0.5)
    if player_choice.upper() == 'ATTACK':
        attack = Player.swing_attack(enemy.baseAC)
        if attack == 'Critical Hit!':
            pdamage = Player.swing_damage() * 2
            print("Incredible! You swing for %d damage!" % (pdamage))
            monster_hp -= pdamage
        elif attack == 'Critical Fail!':
            print("Bad swing! You hurt yourself for 1 damage in the process.")
            player_hp -= 1
        elif attack == 'Hit':
            pdamage = Player.swing_damage()
            print("You swing for %d damage!" % (pdamage))
            monster_hp -=pdamage
        else:
            print("You missed!")
    elif player_choice.upper() == 'FLEE':
        print('You successfully flee combat. Till next time!')
        flee = False
    else:
        print(sorry)
        player_round()
            
def monster_round():
    #monster will always attack
    global player_hp, monster_hp
    print("Player HP: %d      Monster HP: %d" % (player_hp, monster_hp))
    sleep(1)
    #programming specifically for the bear monster. need to invent an attack selector
    bite = enemy.attack_selector(Player.defense)
    if bite[0] == 'Critical Hit!':
        print("The monster does %d damage to you." % (bite[1] * 2))
        player_hp -= bite[1] * 2
    elif bite[0] == 'Critical Fail!':
        print("The monster bites its own tongue for 1 damage.")
        monster_hp -= 1
    elif bite[0] == 'Hit':
        print("The monster does %d damage to you." % (bite[1]))
        player_hp -= bite[1]
    
    
        
   
while monster_hp > 0 and player_hp > 0:
    print("Round %d!" % (counter))
    sleep(0.5)
    player_round()
    if flee == False or monster_hp < 0 or player_hp < 0:
        break
    sleep(0.5)
    monster_round()
    counter += 1

sleep(1)
if player_hp <= 0: 
    print("The %s slays you. Better luck next time." % enemy.name)
if monster_hp <= 0:
    print("You slayed the monster! Congratulations!")
    

