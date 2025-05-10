##DUEL SIMULATOR##
import random

# ITEM CLASS:
class Item:

  def __init__(self, name, damage_type, power, is_legendary = False):
    self.name = name
    self.damage_type = damage_type
    self.power = power
    self.is_legendary = is_legendary

  def __repr__(self):
    description = "{item} deals {power} {damage_type} damage per turn.".format(item = self.name, power = self.power, damage_type = self.damage_type)
    if self.is_legendary == True:
      description += "\n{item} is a LEGENDARY weapon. Only the worthy may wield it.".format(item = self.name)
    return description

# PRE-MADE ITEMS:
gunsword = Item("Gunsword", "Projectile and Slashing", 50, True)

black_sword = Item("Black Sword", "Piercing and Slashing", 50, True)

cloak_of_mist = Item("Cloak of Mist", "Magic", 30)

bb_gun = Item("BB Gun", "Projectile", 10)

dowel = Item("Dowel", "Bludgeoning", 7)

raging_fists = Item("Raging Fists", "Bludgeoning", 40, True)


# FIGHTER CLASS:
class Fighter:

# FIGHTER ATTRIBUTES - name, HP, XP, strength, speed, item, armor, taunt:
  def __init__(self, name, hp = 100, xp = 0, strength = 0, speed = 1, item = None, armor = None, taunt_message = None):
    self.name = name
    self.hp = hp
    self.xp = xp
    self.strength = strength
    self.speed = speed # <-- Speed affects initiative roll at the start of the duel; in a more detailed version of the game, it could also affect blocking ability, or a .dodge() method, etc.
    self.item = item # <-- Keeping it simple with one item per character (for now)
    self.armor = armor
    self.is_blocking = False
    self.block_points = 0
    self.taunt_message = taunt_message

# Fighter String Representation:
  def __repr__(self):
    item_names = self.item.name if self.item else "nothing"
    armor_type = self.armor if self.armor else "no"
    description = """\n{name}'s Stats:
    {name} has {hp} Health Points. 
    {name}'s Strength score is {strength}.
    {name}'s Speed score is {speed}. 
    {name}'s inventory contains: {item_names}. 
    {name} is wearing {armor_type} armor.""".format(
      name = self.name, 
      hp = self.hp, 
      strength = self.strength, 
      speed = self.speed,
      item_names=item_names,
      armor_type = armor_type) #<-- This ensures that if there are no items, "nothing" is displayed instead of a blank space
    if self.item.is_legendary == True:
      description += f"""
    {self.name}'s {self.item.name} is a LEGENDARY weapon with a Power rating of {self.item.power}."""
    return description
  
  # FIGHTER ACTIONS - attack, block, flee, taunt
  # Attack method:
  def attack(self, opponent):
    # Calculate and display damage from the attack:
    opponent_damage = (random.randint(self.strength, self.item.power) * self.strength)
      # How opponent_damage is calculated: A character's strength score represents the minimum base damage that they can inflict, while the power score of their item represents the max damage that they can inflict (therefore, you should make sure that an item's power is higher than the character's strength, or else the item is functionally useless!). The base damage is a random number between their strength score and their item's power, and the final damage is calculated by multiplying base damage times their strength score.
    print(f"\n{self.name} attacks {opponent.name} with {self.item.name}, dealing {opponent_damage} {self.item.damage_type} damage!")
    
    # Check if opponent .is_blocking at the time of the attack:
    if opponent.is_blocking:
      print(f"\n{opponent.name} uses {opponent.item.name} to block {opponent.block_points} damage points from {self.name}'s attack!") # block_points will lessen the opponent's damage score within each conditional check below -- there may be a more concise way to do this...

     # Accounting for opponent's .armor attribute -- Leather resists slashing, Metal resists piercing and projectile, Fabric resists bludgeoning, nothing resists Magic:
    if "Slashing" in self.item.damage_type and opponent.armor == "Leather":
      opponent_damage -= opponent.block_points # Subtracting block points from the damage score (block points are 0 if the opponent is not blocking)
      opponent_damage = opponent_damage * 0.75 # Leather resists 25% of Slashing damage
      opponent_damage_type = self.item.damage_type
      print(f"\n{opponent.name}'s {opponent.armor} armor deflects 25% of the Slashing damage from {self.name}'s {self.item.name}!\n")
      opponent.hp -= opponent_damage
      
    elif ("Projectile" in self.item.damage_type or "Piercing" in self.item.damage_type) and opponent.armor == "Metal":
       opponent_damage -= opponent.block_points
       opponent_damage = opponent_damage * 0.75 # Metal resists 25% of Projectile and Piercing damage
       opponent_damage_type = self.item.damage_type
       opponent.hp -= opponent_damage
       print(f"{opponent.name}'s {opponent.armor} armor deflects 25% of the {self.item.damage_type} damage from {self.name}'s {self.item.name}!")
    
    elif "Bludgeoning" in self.item.damage_type and opponent.armor == "Fabric":
      opponent_damage -= opponent.block_points
      opponent_damage = opponent_damage * 0.75 # Fabric resists 25% of Bludgeoning damage
      opponent_damage_type = self.item.damage_type
      opponent.hp -= opponent_damage
      print(f"{opponent.name}'s {opponent.armor} armor deflects 25% of the {self.item.damage_type} damage from {self.name}'s {self.item.name}!")

    else: #Unarmored opponent, or irresistible (Magic) damage type
      opponent_damage -= opponent.block_points
      opponent.hp -= opponent_damage
    print(f"{opponent.name} takes {opponent_damage} damage from {self.name}'s {self.item.name}!\n")
    print(f"{opponent.name} has {max(0, opponent.hp)} HP remaining!\n")
    opponent.is_blocking = False # Makes it so that the opponent's block only lasts one turn, ending after the attack has been blocked

  # Block method -- How this will work:
    
    # If the character chooses to block, the block score (.block_points) will be calculated using using a random number in their block_capacity (half their item's .power score), and this random number will be multiplied by their .strength score, and their damage will be reduced by the resulting number
  def block(self):
    self.is_blocking = True
    block_capacity = int(self.item.power / 2)
    self.block_points = random.randint(1, block_capacity) * self.strength


  # Flee method -- How it works:
   
    # if a character tries to flee, the success of their flee attempt is calculated using a comparison of their .speed and current .hp against the opponent's .speed and .strength -- a character has less chance of successfully fleeing the more injured they are and the faster and stronger their opponent is -- if they successfully flee, their HP goes to 0 and the opponent wins the duel -- if they unsuccessfully flee, they remain in the duel and it is now the opponent's turn
  def flee(self, opponent):
    print(f"\n{self.name} is attempting to flee from {opponent.name}!")
    if random.randint(1, self.speed) * self.hp > random.randint(1, (opponent.strength * opponent.speed)): # (A successful flee)
      print(f"\n{self.name} manages to get away from {opponent.name}... this time.")
      self.hp = 0 # This will trigger victory for the other opponent
    else: # If the above condition is not met, this means the flee attempt was unsuccessful
      print(f"\n{opponent.name} prevented {self.name} from fleeing! The duel rages on!")


  # Taunt method -- How this works:
   
    # Each fighter will have a signature taunt (in Create-a-Fighter, the player will type out their own taunt string)
    # For now, taunting will not affect the opponent -- in a more detailed version of the game, it could affect the opponent's .morale or .courage rating, or inflict "Psychic" damage calculated based on .courage, .fortitude, or some such attribute
  def taunt(self, opponent):
    if self.taunt_message: # Only works if the character actually has a taunt message
      print(f"{self.name} taunts {opponent.name}: '{self.taunt_message}'")


# PRE-MADE FIGHTERS:
# Bucka
bucka = Fighter("Bucka", 
hp = 1000, 
strength = 10, 
speed = 5,
item = gunsword, 
armor = "Leather",
taunt_message = "HEH-HEH-HEH! Looks like you're 'bout to learn your lesson the hard way, chummy!")

# Bargoth
bargoth = Fighter("Bargoth", 
hp = 1000, 
strength = 20, 
speed = 10,
item = black_sword, 
armor = "Black Metal",
taunt_message = "Now you learn the meaning of pain.")

# LaDonna
ladonna = Fighter("LaDonna", 
hp = 500,
strength = 7, 
speed = 3,
item = cloak_of_mist, 
armor = "Fabric",
taunt_message = "Nyeh heh hehhh! My minions will be having you for supper tonight!")

# Dah
dah = Fighter("Dah", 
strength = 4,
speed = 7,
item = bb_gun,
taunt_message = "Wulp... this is goin' better than I expected.")

# Richad
richad = Fighter("Richad",
strength = 3, 
speed = 7,
item = dowel,
taunt_message = "Hauhhh?")

# The Incredible
incredible = Fighter("The Incredible", 
hp = 1500,
strength = 30, 
speed = 1,
item = raging_fists,
taunt_message = "RAAAAARRR!!!")

# CREATE-A-FIGHTER SYSTEM:
def create_fighter():
  custom_name = input("\nNAME: Enter a name for your Fighter. ")

  custom_hp = int(input(f"\nHP: Next, enter {custom_name}'s Hit Points. This is how much damage {custom_name} can take (to keep the fight interesting, it is recommended that you keep HP below 1000). "))

  custom_strength = int(input(f"\nSTRENGTH: {custom_name}'s Strength determines how effectively they are able to use their weapon for attacking and blocking, and also enables them to stop their opponent from fleeing the duel. Enter a Strength score for {custom_name} (it is recommended that you keep Strength under 30 to keep the duel interesting). "))

  custom_speed = int(input(f"\nSPEED: {custom_name}'s Speed determines their initiative: the faster they are, the more likely they are to land the first blow in a duel. Speed also determines {custom_name}'s ability to flee the duel if they are frightened or hurt, and their ability to stop opponents from fleeing. Enter a Speed score for {custom_name} (it is recommended that you keep Speed under 10). "))

  custom_armor = input(f"""\nARMOR: {custom_name}'s Armor will protect them from certain types of damage: 
  Leather resists Slashing damage. 
  Metal resists Piercing and Projectile damage.
  Fabric resists Bludgeoning damage. 
  Enter one of the following Armor types: Leather, Metal, or Fabric.
  Or, enter 'None' if you want {custom_name} to fight NAKED. """).title()
  if custom_armor != "Leather" and custom_armor != "Metal" and custom_armor != "Fabric" and custom_armor != "None":
    custom_armor = input("\nEnter one of the following Armor options: Leather, Metal, Fabric, or None. ").title()
  print("\n{custom_name} will {custom_armor}.".format(
    custom_name = custom_name, 
    custom_armor = "wear " + custom_armor if custom_armor != "None" else "fight naked.."))

  custom_taunt = input(f"\nTAUNT: If {custom_name} gains the upper hand in a duel, they may taunt their opponent. Enter a Taunt message for {custom_name}: ")

  # Create a custom Item for your fighter -- attributes here: (should this be a nested function?)
  print(f"\nNext, you will create a Weapon for {custom_name} to wield in battle.")
  custom_item_name =  input("\nWEAPON NAME: What is this weapon called? ")

  custom_item_damage_type = input(f"""\nDAMAGE TYPE: Different weapons deal different types of damage, and different damage types can penetrate different types of armor: 
  Slashing damage penetrates Metal and Fabric armor. 
  Piercing damage and Projectile damage penetrate Leather and Fabric armor. 
  Bludgeoning damage penetrates Leather and Metal armor.
  Enter one of the following Damage Types for {custom_item_name}: Slashing, Piercing, Projectile, or Bludgeoning. """).title()
  if custom_item_damage_type != "Slashing" and custom_item_damage_type != "Piercing" and custom_item_damage_type != "Projectile" and custom_item_damage_type != "Bludgeoning":
    custom_item_damage_type = input("\nOops, looks like you entered an invalid Damage Type. Enter one of the following options: Slashing, Piercing, Projectile, or Bludgeoning. ")

  custom_item_power = int(input(f"\nPOWER: Your Weapon's Power rating determines how much damage it can dish out. Enter a Power rating for {custom_item_name} (to keep things interesting, it's recommended that you keep your weapon's Power rating under 50). "))

  custom_item_is_legendary = input(f"\nIs {custom_item_name} a Legendary weapon? If so, enter the true name of Bucka. ")
  if custom_item_is_legendary == "Roger":
    custom_item_is_legendary = True
    print(f"\nTruly, {custom_item_name} is a Legendary weapon! Only the worthy may wield it.")
  else:
    print(f"OK, {custom_item_name} is not a Legendary weapon.\n")

    # Creating the custom Item instance:
  custom_item = Item(name = custom_item_name, 
  damage_type = custom_item_damage_type, 
  power = custom_item_power,
  is_legendary = custom_item_is_legendary)

  # Creating the custom Fighter instance:
  custom_fighter = Fighter(name = custom_name,
  hp = custom_hp,
  strength = custom_strength,
  speed = custom_speed,
  item = custom_item,
  armor = custom_armor,
  taunt_message = custom_taunt
  )

  return custom_fighter


# INITIATE THE GAME:
input("Welcome to DUEL SIMULATOR v1.0, by BuckaSoft LTD (2025, all rights reserved). \nPress Enter to begin. ")

# Message prompting Player 1 to choose: 1) Choose from pre-made Fighters, or 2) Create your own Fighter
p1_welcome_choice = input("\nPlayer 1, prepare to duel. \nYou may choose from one of our pre-made Fighters, or you may create your own. Enter '1' to see our pre-made Fighters, or Enter '2' to create your own Fighter. ")

while p1_welcome_choice != '1' and p1_welcome_choice !='2':
  p1_welcome_choice = input("Looks like you pressed the wrong button, pardner. Enter 1 to see our pre-made Fighters, or Enter '2' to create your own Fighter. ")

# PRE-MADE FIGHTER OPTIONS FOR PLAYER 1:
if p1_welcome_choice == '1':
  p1_fighter_choice = input(""" \nCHOOSE YOUR FIGHTER BY ENTERING THE FIGHTER'S NUMBER:

  1. BUCKA
    Legendary gunslinger, King of Sto.
  2. BARGOTH
    Wielder of the Black Sword.
  3. LADONNA
    Sorceress extraordinaire.
  4. DAH
    Welp...
  5. RICHAD
    Hauh?
  6. THE INCREDIBLE
    'RAAUHHHR!!!'
  
  """)

  if p1_fighter_choice == '1':
    player1 = bucka
  elif p1_fighter_choice == '2':
    player1 = bargoth
  elif p1_fighter_choice == '3':
    player1 = ladonna
  elif p1_fighter_choice == '4':
    player1 = dah
  elif p1_fighter_choice == '5':
    player1 = richad
  elif p1_fighter_choice == '6':
    player1 = incredible
  else:
    p1_fighter_choice = input("You pressed the wrong friggin button, chummy. Enter a number from 1 to 6 to choose your fighter.") # Add option to switch to Create-a-Fighter from here, and add option to switch from Create-a-Fighter to Select-a-Fighter

  # Message confirming fighter selection:
  print("Player 1 has chosen {fighter}! \n".format(fighter = player1.name))
  print(player1)

# CREATE-A-FIGHTER OPTION FOR PLAYER 1:
if p1_welcome_choice == '2':
  print("You chose to create your own Fighter.\n")
  player1 = create_fighter()
  print(player1)

# Message prompting Player 2 to choose: 1) Choose from pre-made Fighters, or 2) Create your own Fighter
p2_welcome_choice = input("\nPlayer 2, prepare to duel. \nYou may choose from one of our pre-made Fighters, or you may create your own. Enter '1' to see our pre-made Fighters, or Enter '2' to create your own Fighter. ")

while p2_welcome_choice != '1' and p2_welcome_choice != '2':
  p2_welcome_choice = input("Looks like you pressed the wrong button, Player 2. Enter 1 to see our pre-made Fighters, or Enter '2' to create your own Fighter. ")

# PRE-MADE FIGHTER SELECTION FOR PLAYER 2:
if p2_welcome_choice == '1':
  p2_fighter_choice = input(""" \nCHOOSE YOUR FIGHTER BY ENTERING THE FIGHTER'S NUMBER:

  1. BUCKA
    Legendary gunslinger, King of Sto.
  2. BARGOTH
    Wielder of the Black Sword.
  3. LADONNA
    Sorceress extraordinaire.
  4. DAH
    Welp...
  5. RICHAD
    Hauh?
  6. THE INCREDIBLE
    'RAAUHHHR!!!'
  
  """)

  if p2_fighter_choice == '1':
    player2 = bucka
  elif p2_fighter_choice == '2':
    player2 = bargoth
  elif p2_fighter_choice == '3':
    player2 = ladonna
  elif p2_fighter_choice == '4':
    player2 = dah
  elif p2_fighter_choice == '5':
    player2 = richad
  elif p2_fighter_choice == '6':
    player2 = incredible
  else:
    p2_fighter_choice = input("You pressed the wrong friggin button, chummy. Enter a number from 1 to 6 to choose your fighter.") # Add option to switch to Create-a-Fighter from here, and add option to switch from Create-a-Fighter to Select-a-Fighter

  # Message confirming fighter selection:
  print("Player 2 has chosen {fighter}! \n".format(fighter = player2.name))
  print(player2)

# CREATE-A-FIGHTER OPTION FOR PLAYER 2:
if p2_welcome_choice == '2':
  print("You chose to create your own Fighter.\n")
  player2 = create_fighter()
  print(player2)


# AUTOMATED BATTLE SYSTEM:

# THE BATTLE FUNCTION:
def battle(player1, player2):

  # Roll initiative to determine who gets the first move:
  player1_initiative = random.randint(1, 20) * player1.speed
  player2_initiative = random.randint(1, 20) * player2.speed
  while player1_initiative == player2_initiative:
    player1_initiative = random.randint(1, 20) * player1.speed
    player2_initiative = random.randint(1, 20) * player2.speed
  if player1_initiative > player2_initiative:
    active_player = player1
    passive_player = player2
  else:
    active_player = player2
    passive_player = player1
    # Add a print message to show which player gets to go first
  print(f"\n{active_player.name} makes the first move!")

  # Nested function to determine active_player's chosen action for the current turn:
  def choose_action(active_player, passive_player):
    choice = None

    # BLOCK method:
    # 2 conditions may trigger .block() chance:
      # 1. active_player HP is less than 75% opponent HP,
      # 2. or opponent's item.power is double active_player's
    
    # 1. HP METHOD FOR BLOCK CHANCE:
    # If active_player's HP is less than 75% of opponent's HP,
    if active_player.hp <= passive_player.hp * 0.75:
      # then active_player's chance of trying to block is determined
      # by a random number in the range of their HP difference
      block_chance = random.randint(1, int(passive_player.hp - active_player.hp))
      # If block_chance is greater than half of HP diff,
      # then active_player will choose .block()
      if block_chance > (passive_player.hp - active_player.hp) / 2:
        choose_block = True

    # 2. ITEM POWER METHOD FOR BLOCK CHANCE:
    # Or, if active_player's item.power is less than half of opponent's,
    elif active_player.item.power <= passive_player.item.power / 2:
      # then active_player's chance of trying to block is determined
      # by a random number in the range of item.power diff
      block_chance = random.randint(1, passive_player.item.power - active_player.item.power)
      # If block_chance is greater than half of item.power diff,
      # then active_player will choose .block()
      if block_chance > passive_player.item.power - active_player.item.power:
        choose_block = True
    
    else: # If neither condition is met, the active player has no chance of trying to block
      choose_block = False
    
    # FLEE method:
    # 2 conditions may trigger .flee() chance: opponent HP is double player HP, or 
    # non-legendary player pitted against legendary player
    if ((passive_player.hp >= active_player.hp * 2) or 
        (active_player.item.is_legendary == False 
         and passive_player.item.is_legendary == True)): 
      # Assess difference in strength between the 2 players
      strength_diff = abs(active_player.strength - passive_player.strength) 
      # Assess fear: a random number in the range of strength_diff 
      fear = random.randint(1, strength_diff)
      # If active_player's fear exceeds half of strength_diff 
      # (this should happen in 50% of cases where the FLEE check is triggered)...
      if fear > strength_diff / 2:
        # ...then active_player will choose to .flee()
        choose_flee = True 

    # Check if BLOCK and FLEE are both True, choose one randomly if they are:
        if choose_block and choose_flee: # < -- this is nested under the Flee check because it will only check for both being True if choose_flee is True
          choice = random.choice(["choose_block", "choose_flee"])
        else:
          choice = "choose_block" if choose_block else "choose_flee"

    # TAUNT method -- How it works (only checks for Taunt conditions if Block and Flee are not chosen):
      # a Fighter has a chance of taunting their opponent if their HP is greater than or equal to twice the opponent's HP, OR if their strength is greater than 2x the opponent's strength, OR if they are Legendary and their opponent is not (the chance of taunting will need to be determined in the Battle System function) 
    elif active_player.hp >= passive_player.hp * 2 or active_player.strength > passive_player.strength * 2 or (active_player.item.is_legendary == True and passive_player.item.is_legendary == False):
      # Make it so that the more powerful player is not stuck taunting forever!
      taunt_chance = random.randint(1, (max(active_player.strength, passive_player.strength) - min(active_player.strength, passive_player.strength)))
      if taunt_chance > 0.75 * (max(active_player.strength, passive_player.strength) - min(active_player.strength, passive_player.strength)): # <-- If the random taunt chance is greater than 75% of the difference in strength, then the player will choose to taunt -- to make gameplay more dynamic, could add a .cockiness attribute that effects this multiplier, but for now keep it simple at 0.75 for all players
        choose_taunt = True
      else:
        choose_taunt = False
      if choose_taunt == True:
        choice = "choose_taunt"
    
    # Executing the player's chosen action:
    if choice == "choose_block":
      active_player.block()
    elif choice == "choose_flee":
      active_player.flee(passive_player)
    elif choice == "choose_taunt":
      active_player.taunt(passive_player)
    else:
      active_player.attack(passive_player)
    
    
  
 # Battle Loop:
  while player1.hp > 0 and player2.hp > 0: # Battle continues as long as both players are alive
    # Active player makes their move
    choose_action(active_player, passive_player)
    # Switch players -- it is now the other player's turn:
    active_player, passive_player = passive_player, active_player
  
  if player1.hp <= 0:
    print(f"\n{player1.name} has been vanquished! {player2.name} wins! \nGAME OVER")
  
  if player2.hp <= 0:
    print(f"\n{player2.name} has been vanquished! {player1.name} wins! \nGAME OVER")

battle(player1, player2)

## END OF PROGRAM (for now) ##