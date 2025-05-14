# Duel Simulator
A simple text-based Python terminal game that simulates duels between various characters.

## Background
The purpose of _Duel Simulator_ was to practice my basic object-oriented programming skills in Python. This project was intended as a low-stakes opportunity to make something fun while developing foundational skills, so I did not think too hard about what I was going to make. One of the examples that Codecademy provided was a Pokemon game, and after looking over the code for the Pokemon game, the idea quickly occurred to me to create my own turn-based combat game featuring stylized characters from my personal mythos.

At first, I wanted the players to control the Fighters’ actions, but as I got into the process and started testing out the code, I thought it would be more interesting to try to make the Fighters autonomous: the players would simply choose (or create) their Fighters, then pit them against one another and watch what happens. Given the Fighters’ limited range of actions, I figured this would make “gameplay” more riveting and unpredictable than having the players choose each of the Fighters’ actions in real time.

## How It Works
The program uses the ``random`` library, custom ``Fighter`` and ``Item`` classes, and a variety of interactive attributes and methods to generate dynamic, unpredictable duels.

I began by defining my ``Item`` and ``Fighter`` classes: 

### ``Item``
``Item``s have a ``.name``, ``.damage_type``, and ``.power`` rating. An ``Item``'s ``.damage_type`` interacts with the opponent's ``.armor``, with different types of armor offering some resistance against different types of damage. ``Item``s also have an ``.is_legendary`` attribute with a default value of ``False``. When ``Item.is_legendary`` is set to ``True``, the ``Fighter`` wielding the ``Item`` may strike ``fear`` into the heart of his opponent, causing him to ``.flee()`` the duel.

### ``Fighter``
``Fighter``s have a ``.name``, ``.hp``, ``.strength``, ``.speed``, and ``.armor``. Each ``Fighter`` also has an ``.item`` (a weapon) and a preset ``.taunt_message`` that they may shout at their opponent if they gain the upper hand during the duel. Additionally, ``Fighter``s have ``.is_blocking`` and ``.block_points`` attributes, set to ``False`` and ``0`` respectively, which update if their ``.block()`` method is triggered during the duel.

A ``Fighter``'s available actions are ``.attack()``, ``.block()``, ``.flee()``, and ``.taunt()``.

#### ``Fighter.attack()``
This method takes ``self`` and ``opponent`` as arguments. 

The minimum damage that a character can inflict is either their ``.strength`` or their ``Item``'s ``.power`` rating, whichever number is lower. The maximum damage that they can inflict is their ``.strength`` score multiplied by ``Item.power``. Base damage is a ``random`` integer in the range between their ``.strength`` score and ``Item.power``, and final damage is base damage multiplied by ``.strength``. The final damage number deducted from the opponent's ``.hp``. 

If ``opponent.is_blocking`` at the time of the ``.attack()``, then the damage is reduced by the opponent's current ``.block_points``.

The ``opponent``'s ``.armor`` also affects how much damage they take from the attack. ``"Leather"`` armor resists ``"Slashing"`` damage, ``"Metal"`` resists `"Piercing"` and `"Projectile"` damage, "Fabric" resists `"Bludgeoning"`, and nothing resists `"Magic"`.

#### `Fighter.block()`
If a character chooses to `.block()`, then their `.is_blocking` attribute is set to `True`, their `.block_points` are calculated using a `random` integer in the range of half their weapon's `.power` score, multiplied by their `.strength` score. Their incoming damage is then reduced by their `.block_points`. Their `is_blocking` attribute is set back to `False` at the end of their opponent's `.attack()`, ensuring that they do not continue blocking into the next turn.

#### `Fighter.flee()`
If a character tries to `.flee()`, the success of their flee attempt is calculated using a comparison of their `.speed` and current `.hp` against the opponent's `.speed` and .`strength`. A character has less chance of successfully fleeing the more injured they are and the faster and stronger their opponent is. If they successfully flee, their `.hp` goes to `0` and the opponent wins the duel. If they unsuccessfully flee, they remain in the duel and it is now the opponent's turn.

Then, I wrote functions 

How each Fighter method works

How Fighters choose their actions during gameplay

Functions that drive the game


### Additional features
I had plenty of other ideas for game features, including, but not limited to: saveable ``Player`` profiles, more and varied types of ``Item``s, more complex ``Fighter`` attributes and behaviors, ``Fighter.xp`` and a leveling system, more dynamic action descriptions, and perhaps even a “story mode." However, in order to limit scope creep and continue on my learning journey, I decided to set a hard limit (for now) on the game’s features.


## Image

## Conclusion
I learned a lot by making _Duel Simulator_ and I had fun doing it. Perhaps most importantly of all, I learned just how much time and care can go into even a simple program like this.
