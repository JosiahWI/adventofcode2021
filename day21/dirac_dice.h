#ifndef DIRAC_DICE_H_INCLUDED
#define DIRAC_DICE_H_INCLUDED

#include <sstream>

class DiracDice
{
public:
    DiracDice(int* playerPositions, int players);
    ~DiracDice();
    std::stringstream toString();
    int playUntilScore(int score);
    bool noScoresAbove(int score);
    int losingScore();
private:
    int m_players;
    int* m_playerPositions;
    int* m_playerScores;
};

#endif // DIRAC_DICE_H_INCLUDED
