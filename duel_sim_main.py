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

# FIGHTER ATTRIBUTES:
  def __init__(self, 
               name, 
               hp = 100, 
               xp = 0, 
               strength = 0, 
               speed = 1, 
               item = None, 
               armor = None, 
               taunt_message = None):
    self.name = name
    self.hp = hp
    self.xp = xp
    self.strength = strength
    self.speed = speed
    self.item = item
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
      armor_type = armor_type)
    if self.item.is_legendary == True:
      description += f"""
    {self.name}'s {self.item.name} is a LEGENDARY weapon with a Power rating of {self.item.power}."""
    return description
  
  # FIGHTER ACTIONS - attack, block, flee, taunt
  
  # Attack method:
  def attack(self, opponent):
    # Calculate and display damage from the attack:
    opponent_damage = (random.randint(min(self.strength, self.item.power), 
                                      max(self.strength, self.item.power)) 
                                      * self.strength)
      # How opponent_damage is calculated: 
      # The minimum damage that a character can inflict 
      # is either their strength or their item's power,
      # whichever number is lower.
      # The max damage they can inflict is
      # their strength multiplied by their item's power. 
      # Base damage is a random number in the range between
      # their strength score and their item's power, 
      # and final damage is base damage multiplied by strength score.
    print(f"\n{self.name} attacks {opponent.name} with {self.item.name}, dealing {opponent_damage} {self.item.damage_type} damage!")
    
    # Check if opponent .is_blocking at the time of the attack:
    if opponent.is_blocking:
      print(f"\n{opponent.name} uses {opponent.item.name} to block {opponent.block_points} damage points from {self.name}'s attack!")

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
    opponent.is_blocking = False

  # Block method -- How this works:
    
    # If the character chooses to block, their block score (.block_points)
    # is calculated using a random number 
    # in the range of half their item's .power score, 
    # and this random number is multiplied by their .strength score, 
    # and their damage is reduced by the resulting number
  def block(self):
    self.is_blocking = True
    block_capacity = int(self.item.power / 2)
    self.block_points = random.randint(1, block_capacity) * self.strength
    print(f"{self.name} gets into a defensive stance...")

  # Flee method -- How it works:
   
    # if a character tries to flee, 
    # the success of their flee attempt is calculated using a comparison of
    # their .speed and current .hp against the opponent's .speed and .strength.
    # A character has less chance of successfully fleeing 
    # the more injured they are and the faster and stronger their opponent is.
    # If they successfully flee, their HP goes to 0 
    # and the opponent wins the duel.
    # If they unsuccessfully flee, they remain in the duel
    # and it is now the opponent's turn.
  def flee(self, opponent):
    print(f"\n{self.name} is attempting to flee from {opponent.name}!")
    if (random.randint(1, self.speed) * self.hp 
        > random.randint(1, (opponent.strength * opponent.speed))):
      print(f"\n{self.name} manages to get away from {opponent.name}... this time.")
      self.hp = 0 # This will trigger victory for the other opponent
    else:
      print(f"\n{opponent.name} prevented {self.name} from fleeing! The duel rages on!")


  # Taunt method:
  def taunt(self, opponent):
    if self.taunt_message: # Only works if the character actually has a taunt message
      print(f"\n{self.name} taunts {opponent.name}: '{self.taunt_message}'")

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

# FIGHTER SELECTION FUNCTION: 
def select_fighter():
  # Fighter options:
  def fighter_assign():
    fighter_choice = int(input(""" \nCheck a Fighter's Stats by entering the Fighter's number:

1. BUCKA
  Legendary gunslinger, King of Sto.
2. BARGOTH
  Wielder of the Black Sword.
3. LADONNA
  Sorceress extraordinaire.
4. DAH
  Wulp...
5. RICHAD
  Hauh?
6. THE INCREDIBLE
  'RAAUHHHR!!!'

"""))

    while fighter_choice not in range(1, 7):
      fighter_choice = int(input("""
                            You pressed the wrong friggin button, ya dubba. 
                            Enter a number from 1 to 6 to choose your Fighter."""))
    if fighter_choice == 1:
      player = bucka
    elif fighter_choice == 2:
      player = bargoth
    elif fighter_choice == 3:
      player = ladonna
    elif fighter_choice == 4:
      player = dah
    elif fighter_choice == 5:
      player = richad
    elif fighter_choice == 6:
      player = incredible
    return player
  
  # Assign selected Fighter to player:
  player = fighter_assign()

  # Confirm player's Fighter selection:
  def confirm_selection(player):

    while True:
      print(f"""\nYou have chosen {player.name.upper()}!

        {player}

    """)
      confirm_selection = input(f"\nAre you sure you want to continue with {player.name}? Y / N ").upper()
      if confirm_selection == 'Y':
        input(f"\nFighter selection confirmed: {player.name}. Press Enter to continue. ")
        return player
      elif confirm_selection == 'N':
        print("\nOK, choose a different Fighter.\n")
        player = fighter_assign()
      else:
        confirm_selection = input(f"\nInvalid input. \nPlease enter Y to confirm {player.name} as your chosen Fighter, or enter N to choose a different Fighter. Y / N ")
  
  confirm_selection(player)

  # Return player object to function call:
  return player
 
    # Add option to switch to Create-a-Fighter from here, and add option to switch from Create-a-Fighter to Select-a-Fighter
    
# CREATE-A-FIGHTER FUNCTION:
def create_fighter():
  dubba_counter = 0
  custom_name = input("\nNAME: Enter a name for your Fighter. ")
  while custom_name == '':
    dubba_counter += 1
    custom_name = input("\nPlease enter a name for your Fighter before continuing. ")
    if dubba_counter > 2:
      print("""
      You friggin' dubbah, don't you know how to follow instructions?
      Now your Fighter's name is going to be DUBBAH. Serves you right! HEh-Heh-hEh.""")
      custom_name = "Dubbah"

  custom_hp = input(f"\nHP: Next, enter {custom_name}'s Hit Points. This is how much damage {custom_name} can take (to keep the fight interesting, it is recommended that you keep HP below 1000). ")
  while True:
    try:
      custom_hp = int(custom_hp)
      print(f"\n{custom_name}'s HP is set to {custom_hp}.")
      break
    except ValueError:
      custom_hp = input(f"\nUhhh... enter a valid number for {custom_name}'s HP. ")
      dubba_counter += 1
      if dubba_counter > 4:
        custom_hp = 100
        print(f"\nYou can't seem to figure this out, so I'll set your HP to 100, how about that? Friggin dub... Sheesh... ")

  custom_strength = input(f"\nSTRENGTH: {custom_name}'s Strength determines how effectively they are able to use their weapon for attacking and blocking, and also enables them to stop their opponent from fleeing the duel. Enter a Strength score for {custom_name} (it is recommended that you keep Strength under 30 to keep the duel interesting). ")
  while True:
    try:
      custom_strength = int(custom_strength)
      while custom_strength > 100:
        custom_strength = input(f"\nYou friggin' numbskull, I ain't lettin' you set {custom_name}'s Strength that high. Try a lower number. ")
      print(f"\n{custom_name}'s Strength is set to {custom_strength}.")
      break
    except ValueError:
      custom_strength = input("What kinda dubbah are you? That ain't a number. Enter a NUMBER. ")

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
# start_game() function enables replayability
# when the duel ends:
def start_game():

  input("Welcome to DUEL SIMULATOR v1.0, by BuckaSoft LTD (2025, all rights reserved). \nPress Enter to begin. ")

  # Message prompting Player 1 to choose: 
  # 1) Choose from pre-made Fighters, or 
  # 2) Create your own Fighter
  p1_welcome_choice = input("\nPlayer 1, prepare to duel. \nYou may choose from one of our pre-made Fighters, or you may create your own. \nEnter '1' to see our pre-made Fighters, or Enter '2' to create your own Fighter. ")

  while p1_welcome_choice != '1' and p1_welcome_choice !='2':
    p1_welcome_choice = input("Looks like you pressed the wrong button, pardner. Enter 1 to see our pre-made Fighters, or Enter '2' to create your own Fighter. ")
  # Call select_fighter if welcome_choice = '1'

  # PRE-MADE FIGHTER OPTIONS FOR PLAYER 1:
  if p1_welcome_choice == '1':
    player1 = select_fighter()

  # CREATE-A-FIGHTER OPTION FOR PLAYER 1:
  if p1_welcome_choice == '2':
    print("You chose to create your own Fighter.\n")
    player1 = create_fighter()
    print(player1)

  # Message prompting Player 2 to choose: 
  # 1) Choose from pre-made Fighters, or 
  # 2) Create your own Fighter
  p2_welcome_choice = input("\nPlayer 2, prepare to duel. \nYou may choose from one of our pre-made Fighters, or you may create your own. \nEnter '1' to see our pre-made Fighters, or Enter '2' to create your own Fighter. ")

  while p2_welcome_choice != '1' and p2_welcome_choice != '2':
    p2_welcome_choice = input("Looks like you pressed the wrong button, Player 2. \nEnter 1 to see our pre-made Fighters, or Enter '2' to create your own Fighter. ")

  # PRE-MADE FIGHTER SELECTION FOR PLAYER 2:
  if p2_welcome_choice == '1':
    player2 = select_fighter()

  # CREATE-A-FIGHTER OPTION FOR PLAYER 2:
  if p2_welcome_choice == '2':
    print("You chose to create your own Fighter.\n")
    player2 = create_fighter()
    print(player2)
  
  return player1, player2

# AUTOMATED DUEL SYSTEM:
# THE DUEL FUNCTION:
def duel(player1, player2):

  input(f"""
        Fighters have been chosen...
        {player1.name} versus {player2.name}...
        Who will be victorious?

        PRESS ENTER TO BEGIN THE DUEL.""")

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

    # FLEE option:
    # 2 conditions may trigger .flee() chance: 
      # 1. HP is less than 30% opponent's HP, or 
      # 2. non-legendary player pitted against legendary player
    if ((active_player.hp <= passive_player.hp * 0.3) or 
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
        choice = "choose_flee"
      else:
        choose_flee = False
    else:
      choose_flee = False
    
    # BLOCK option:
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
        # choice = "choose_block"
      else:
        choose_block = False

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
        # choice = "choose_block"
      else:
        choose_block = False
    
    else: 
      # If neither condition is met, active_player will not block
      choose_block = False
    
    # If BLOCK and FLEE are both True, choose one randomly:
        # if choose_block and choose_flee:
        #   choice = random.choice(["choose_block", "choose_flee"])

    # TAUNT option:
      # 3 conditions may trigger .taunt() chance:
        # 1. active_player's HP is double opponent's HP, or
        # 2. strength is double opponent's strength, or
        # 3. Legendary fighter against non-legendary
    if (active_player.hp >= passive_player.hp * 2 
          or active_player.strength > passive_player.strength * 2 
          or (active_player.item.is_legendary == True 
              and passive_player.item.is_legendary == False)):
      # Randomizing taunt_chance using strength_diff
      # ensures that player is not stuck taunting forever!
      if active_player.strength > passive_player.strength:
        strength_diff = abs(active_player.strength - passive_player.strength)
        taunt_chance = random.randint(1, strength_diff)
        # Player chooses to taunt if random taunt_chance
        # exceeds 75% of strength_diff
        # (i.e. in 25% of cases where taunt_chance is triggered)
        if taunt_chance > 0.75 * strength_diff:
          choose_taunt = True
        else:
          choose_taunt = False
    else:
      choose_taunt = False
        # if choose_taunt == True:
        #   choice = "choose_taunt"
    
    # Executing the player's chosen action:
    if choose_block:
      active_player.block()
    elif choose_flee:
      active_player.flee(passive_player)
    elif choose_taunt:
      active_player.taunt(passive_player)
    else:
      active_player.attack(passive_player)
    
 # Battle Loop:
 # Battle continues as long as both players are alive
  while player1.hp > 0 and player2.hp > 0:

    # Active player makes their move
    choose_action(active_player, passive_player)

    if player1.hp <= 0:
      print(f"""
      {player1.name} has been vanquished! {player2.name} wins! 
            
      GAME OVER""")
      break

    if player2.hp <= 0:
      print(f"""
      {player2.name} has been vanquished! {player1.name} wins! 
            
      GAME OVER""")
      break

    # User inputs to trigger the next turn:
    input("\nPress Enter to see what happens next!") 
    
    # Switch players -- it is now the other player's turn:
    active_player, passive_player = passive_player, active_player

# On/Off Switch for Replayability:
game_on = True

# GAMEPLAY LOOP:
while game_on == True:
  player1, player2 = start_game()
  duel(player1, player2)

# RESTART GAME OPTION AT END OF DUEL:
  restart_choice = input("\nWould you like to play again? Y / N ").upper()
  if restart_choice == 'Y':
    continue
  else:
    print("""
    GAME OVER
    
    Thank you for playing DUEL SIMULATOR!""")
    break


## END OF PROGRAM (for now) ##