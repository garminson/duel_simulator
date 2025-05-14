# Duel Simulator
_Duel Simulator_ is a simple text-based Python terminal game for two players that simulates duels between various characters.

Below is a technical description of this project. If you'd like to skip ahead to How to Play, you can scroll to the bottom or [click here](#how-to-play).

## Background
My purpose in creating _Duel Simulator_ was to practice my basic object-oriented programming skills in Python. This project was intended as a low-stakes opportunity to make something fun while developing foundational skills, so I did not think too hard about what I was going to make. One of the examples that Codecademy provided was a Pokemon game, and after looking over the code for the Pokemon game, the idea quickly occurred to me to create my own turn-based combat game featuring stylized characters from my personal mythos.

At first, I wanted the players to control the Fighters’ actions, but as I got into the process and started testing out the code, I thought it would be more interesting to try to make the Fighters autonomous: the players would simply choose (or create) their Fighters, then pit them against one another and watch what happens. Given the Fighters’ limited range of actions, I figured this would make “gameplay” more riveting and unpredictable than having the players choose each of the Fighters’ actions in real time.

## How It Works
The program uses the ``random`` library, custom ``Fighter`` and ``Item`` classes, and a variety of interactive attributes and methods to generate dynamic, unpredictable duels.

I began by defining my ``Item`` and ``Fighter`` classes: 

### ``Item``
``Item``s have a ``.name``, ``.damage_type``, and ``.power`` rating. An ``Item``'s ``.damage_type`` interacts with the opponent's ``.armor``, with different types of armor offering some resistance against different types of damage. ``Item``s also have an ``.is_legendary`` attribute with a default value of ``False``. When ``Item.is_legendary`` is set to ``True``, the ``Fighter`` wielding the ``Item`` may strike ``fear`` into the heart of his opponent, causing him to ``.flee()`` the duel.

### ``Fighter``
``Fighter``s have a ``.name``, ``.hp``, ``.strength``, ``.speed``, and ``.armor``. Each ``Fighter`` also has an ``.item`` (a weapon) and a preset ``.taunt_message`` that they may shout at their opponent if they gain the upper hand during the duel. Additionally, ``Fighter``s have ``.is_blocking`` and ``.block_points`` attributes, set to ``False`` and ``0`` respectively, which update if their ``.block()`` method is triggered during the duel.

A ``Fighter``'s available actions are ``.attack()``, ``.block()``, ``.flee()``, and ``.taunt()``:

#### ``Fighter.attack()``
This method takes ``self`` and ``opponent`` as arguments. 

The minimum damage that a character can inflict is either their ``.strength`` or their ``Item``'s ``.power`` rating, whichever number is lower. The maximum damage that they can inflict is their ``.strength`` score multiplied by ``Item.power``. Base damage is a ``random`` integer in the range between their ``.strength`` score and ``Item.power``, and final damage is base damage multiplied by ``.strength``. The final damage number deducted from the opponent's ``.hp``. 

If ``opponent.is_blocking`` at the time of the ``.attack()``, then the damage is reduced by the opponent's current ``.block_points``.

The ``opponent``'s ``.armor`` also affects how much damage they take from the attack. ``"Leather"`` armor resists ``"Slashing"`` damage, ``"Metal"`` resists `"Piercing"` and `"Projectile"` damage, "Fabric" resists `"Bludgeoning"`, and nothing resists `"Magic"`.

#### `Fighter.block()`
If a character chooses to `.block()`, then their `.is_blocking` attribute is set to `True`, their `.block_points` are calculated using a `random` integer in the range of half their weapon's `.power` score, multiplied by their `.strength` score. Their incoming damage is then reduced by their `.block_points`. Their `is_blocking` attribute is set back to `False` at the end of their opponent's `.attack()`, ensuring that they do not continue blocking into the next turn.

#### `Fighter.flee()`
If a character tries to `.flee()`, the success of their flee attempt is calculated using a comparison of their `.speed` and current `.hp` against the opponent's `.speed` and .`strength`. A character has less chance of successfully fleeing the more injured they are and the faster and stronger their opponent is. If they successfully flee, their `.hp` goes to `0` and the opponent wins the duel. If they unsuccessfully flee, they remain in the duel and it is now the opponent's turn.

#### `Fighter.taunt()`
This action was written to add amusement to the gameplay experience. Each pre-made `Fighter` has a signature `taunt_message`, and the user can enter a custom `taunt_message` if they choose to create their own `Fighter`. I originally intended for `.taunt()` to deal some kind of "psychic damage" to the opponent, or perhaps lower a `.morale` attribute in the opponent, but I put this aspiration on hold for the sake of getting the project done.

After creating my `Item` and `Fighter` classes, and a few instances of each, I then wrote gameplay functions:

#### `start_game()`
This welcomes the user to _Duel Simulator_, then prompts the user to either enter the pre-made Fighter selection menu, thereby calling the `select_fighter()` function, or create their own Fighter, thereby calling the `create_fighter()` function. The process repeats for both players.

#### `select_fighter()`
Presents the user with a list of pre-made Fighters to choose from. Upon selecting a Fighter, the user is show the Fighter's stats, and asked if they wish to continue with this Fighter. If not, they may choose a different Fighter.

#### `create_fighter()`
Guides the user through the creation of their own custom Fighter, with humorous error handling messages displayed in case the user enters an invalid value at any stage of the Fighter creation process.

#### `duel()`
This function is called after both players have either chosen or created Fighters. The `duel()` function takes two arguments: `player1` and `player2`, which are first defined in the `select_fighter()` or `create_fighter()` function call within the `start_game()` function.

The duel begins with an initiative roll to determine which Fighter gets the first move. Initiative is calculated DnD-style using random integers between 1 and 20 multiplied by each Fighter's speed.

Whichever Fighter rolls higher initiative is assigned to `active_player`, meaning it is their turn to make a move, while the other Fighter is assigned to `passive_player`. After the `active_player` makes their move, the roles switch. This loop continues as long as both Fighters' HP are above 0.

During their turn, a `Fighter` chooses from one of their 4 available actions: 1) `.attack()`, 2) `.block()`, 3) `.flee()`, or 4) `.taunt()`. The `duel()` function checks a series of conditions to evaluate whether the `Fighter` should block, flee, or taunt, and if none of these conditions are met, the Fighter defaults to `.attack()`. 

A basic overview of the `Fighter` decision-making logic is as follows:

**When to `.block()`**: 2 conditions may trigger a chance of trying to `.block()`: If `active_player`'s `.hp` is less than 75% of the opponent's (`passive_player`'s) `.hp`, _or_ if their opponent's `Item` has double the `.power` of their own. For the HP method, the `active_player`'s chance of trying to block is determined by a random number in the range of the HP difference between the two `Fighter`s. If this random number is greater than half of the total difference in HP, then the `active_player` will choose to `.block()`. For the `Item.power` method, `active_player`'s chance of trying to block is determined by a random number in the range of the `item.power` difference between the two `Fighter`s. If this random number is greater than half of the `item.power` difference, then `active_player` will choose to `.block()`.

**When to `.flee()`**: 2 conditions may trigger a chance of `active_player` trying to `.flee()`: If their HP is less than 30% of their opponent's HP, or if they are a non-legendary player pitted against a legendary player (one wielding a legendary weapon). In both of these cases, the active_player's chance of trying to .flee(), i.e. their `fear`, is calculated in the same way: A random number in the range of the `.strength` difference between the two `Fighter`s. If the `active_player`'s `fear` exceeds half of the strength difference, then the `active_player` will try to `.flee()` the duel. Whether their `.flee()` attempt is successful or not depends on several factors described above in the section on `Fighter` methods.

In case `active_player` chooses both `.block()` and `.flee()`, they will default to `.block()`.

**When to `.taunt()`**: 3 conditions may trigger a chance of `active_player` trying to `.taunt()`: 1) their `.hp` is double their opponent's `.hp`, 2) their `strength` is double their opponent's `strength`, or 3) they are a legendary `Fighter` pitted against a non-legendary `Fighter`. If any of these conditions are met, `active_player`'s chance of trying to `.taunt()` is determined by a random number in the range of the difference in `strength` between the two `Fighter`s (in the unlikely event that the 2 `Fighter`s are of equal `strength`, the taunt chance is a random number between 1 and 10). The `active_player` will choose to `.taunt()` if this random `taunt_chance` exceeds 75% of the difference in `strength` (or, if they are of equal `strength`, if the `taunt_chance` is greater than `7.5`.

**When to `.attack()`**: If the character does not choose to `.block()`, `.flee()`, or `.taunt()`, they will automatically choose to `.attack()`.

## Additional features
I had plenty of other ideas for game features, including, but not limited to: saveable ``Player`` profiles, more and varied types of ``Item``s, more complex ``Fighter`` attributes and behaviors (e.g. `.courage` or `.morale`, finisher moves, multi-`Item` inventories), ``Fighter.xp`` and a leveling system, more dynamic action descriptions, and perhaps even a “story mode." However, in order to limit scope creep and continue on my learning journey, I decided to set a hard limit (for now) on the game’s features.

## How to Play
1. Download the latest version of Python
2. Download [duel_sim_main.py]((https://github.com/garminson/duel_simulator/blob/main/duel_sim_main.py)) or clone this repository
3. Open the Terminal app on your computer
4. Run the game by entering the following command in Terminal: `python3 duel_sim_main.py`
5. Follow the on-screen directions!
