// part 1

#include "dirac_dice.h"
#include <iostream>

namespace
{
    constexpr int players { 2 };
    constexpr int winningScore { 1000 };
}

int main()
{
    int playerPositions[players];
    for (int i { 0 }; i < players; ++i)
    {
        std::cin.ignore(1024, ':');
        std::cin >> playerPositions[i];
    }

    DiracDice dice { playerPositions, players };
    int diceRolls { dice.playUntilScore(winningScore) };
    std::cout << "Rolled " << diceRolls << " times.\n";
    std::cout << "Part 1: " << diceRolls * dice.losingScore() << '\n';
}
