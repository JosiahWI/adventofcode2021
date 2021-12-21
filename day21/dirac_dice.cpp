#include "dirac_dice.h"
#include <iostream> // debugging
#include <string>

DiracDice::DiracDice(int* playerPositions, int players) :
    m_playerPositions { playerPositions },
    m_playerScores { new int[players] {} },
    m_players { players }
{
}

DiracDice::~DiracDice()
{
    delete[] m_playerScores;
}

std::stringstream DiracDice::toString()
{
    // space separated positions of the players
    std::stringstream oss {};
    for (int i { 0 }; i < m_players; ++i)
    {
        oss << m_playerPositions[i] << ' ';
    }
    oss << '\n';

    // space separated scores of the players
    for (int i { 0 }; i < m_players; ++i)
    {
        oss << m_playerScores[i] << ' ';
    }
    oss << '\n';

    return oss;
}

int DiracDice::playUntilScore(int score)
{
    int diceRolls { 0 };
    int nextDiceValue { 1 };
    while (true)
    {
        for (int i { 0 }; i < m_players; ++i)
        {
            if (!noScoresAbove(score - 1))
            {
                return diceRolls;
            }
            // each player roles the dice three times
            for (int j { 0 }; j < 3; ++j)
            {
                m_playerPositions[i] += nextDiceValue;
                m_playerPositions[i] %= 10;
                if (m_playerPositions[i] == 0)
                {
                    m_playerPositions[i] = 10;
                }

                ++nextDiceValue;
                if (nextDiceValue > 100)
                {
                    nextDiceValue %= 100;
                }
            }
            m_playerScores[i] += m_playerPositions[i];
            diceRolls += 3;
        }    
    }
}

bool DiracDice::noScoresAbove(int score)
{
    for (int i { 0 }; i < m_players; ++i)
    {
        if (m_playerScores[i] > score)
        {
            return false;
        }
    }
    // if no player has a score > score
    return true;
}

int DiracDice::losingScore()
{
    int min { m_playerScores[0] };
    for (int i { 0 }; i < m_players; ++i)
    {
        if (m_playerScores[i] < min)
        {
            min = m_playerScores[i];
        }
    }

    return min;
}
