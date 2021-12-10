#ifndef BINGO_H_INCLUDED
#define BINGO_H_INCLUDED

#include <array>
#include <fstream>

namespace bingo
{

    struct Square
    {
        int value { -1 };
        bool isMarked { false };
    };
    using rowColumn_t = std::array<Square, 5>;
    using rawBoard_t = std::array<rowColumn_t, 5>;

    class Board
    {
    public:
        Board(std::ifstream &ifs);
        void printBoard() const;
        bool isSolved() const;
        void mark(int value);
        void finish();
        bool isFinished() const;
        int sumUnmarked();

    private:
        bool checkRows() const;
        bool checkColumns() const;
        rawBoard_t rawBoard;
        bool finished { false };
    };

}

#endif // BINGO_H_INCLUDED

