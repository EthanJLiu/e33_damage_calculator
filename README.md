# e33_damage_calculator
This is an endgame damage calculator app for Clair Obscur: Expedition 33 using python's tkinter library. 
I made this both for my own personal use, and as a way to practice coding projects from scratch

How to Use:

Select a character, select its weapon, skill, and check off any buffs and pictos that you want to use.
You can adjust the weapon level as needed. The calculator will display your base attack power(no stat scaling) 
and your total attack damage seen in the in game stat screen. Below it will show your expected single hit skill damage
with and without conditions met and total skill damage with and without conditions met. Checking off buffs and pictos will boost
the damage displayed on screen accordingly. Conditions met/not met refers to any conditions highlighted in skill descriptions
that will increase the damage(Ex: Lune's stains)

There are four pictos that have hidden damage bonuses not displayed in game: Sweet Kill, Dead Energy II, First Strike, and Teamwork
- Teamwork has an additional 11% increased damage on top of its displayed 10% increased damage
- Sweat Kill, Dead Energy II, and First Strike all give 10% more damage despite not showing it in their in-game descriptions
    - It is unclear whether these are cumulative or multiplicative bonuses 

IMPORTANT: The displayed damage may not show the exact damage you will do in game. As weapons level up, their damage increases.
However, the rate at which the damage increases, although similar, is not the exact same for each weapon. Also, the game rounds
the weapons damage, but there is seemingly no pattern to when it decides to rounds up or down.
Despite the slight inconsistencies, the LEADING COUPLE DIGITS should still be mostly correct

The calculator has a number of features that have not been implemented(highlighted below); however this has been narrowed down to 
just a couple multiplicative bonuses, so simply take the displayed damage and multiply it by whatever bonus that isn't implemented

Known Issues/unfinished features:
- Weapon specific damage bonuses
- Character specific bonuses (Maelle's stance, Verso's Perfection) can be applied to any character
- You cannot manually adjust your stat distribution. The calculator assumes you have 99 points into might
  and each of your weapons affinities, which is optimal for damage
- Some buffs are not compatible with each other. For example, Full Strength and At Death's Door can both be selected
  even though it is impossible to have both active in game(Full Strength requires full health; At Death's Door require <= 10% hp)
- Sireso and Greater Powerful can be checked at the same time even though they cannot be in game
    - Sireso's scaling may not be accurate
- Only greater powerful and greater defenseless available
- Gradient Fighter scales non-gradient attacks. For now, un-check it if you are using non-gradients

Assumptions
- It is assumed that you have 100% critical chance(at endgame, it is extremely easy to achieve this with pictos)
    - Monoco:
        - Chevelier’s piercing assumes three shields
        - Creation void only works for final scaled damage
        - Cultist’s blood assumes 90% hp donation
        - Cultists slashes assumes 1 hp remaining
        - Lampmaster light assumes 6th cast
    - Verso:
        - Skills display boost from the inherent perfection bonus from the skill(global perfection bonus not implements)
        - Sireso not implemented
        - Berserk slash assumes 1% hp remaining
        - Speed burst has max speed difference bonus of 2x
    - Lune:
        - Electrify and lightening dance calculate damage based on the 2x hits from crits
    - Maelle:
        - Burning canvas assumes 100 burn stacks + the additional added burn stacks from the hits for 11.2 conditional scaling
        - Combustion assumes max of 10 burn stacks consumed
        - Revenge assume 3 hits
        - Gustave’s hommage not implemented
    - Sciel:
        - No shadow bringer support
        - Sciel assumes 20 foretell
            - 40 for Endslice