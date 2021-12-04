#include "bingo.h"
#include <cstddef>
#include <fstream>
#include <iostream>
#include <limits>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

namespace bingo
{

    Board::Board(std::ifstream &ifs) : rawBoard {}
    {
        for (rowColumn_t &row : rawBoard)
        {
            for (Square &square : row)
            {
                ifs >> square.value;
            }
        }
    }

    void Board::printBoard() const
    {
        for (const rowColumn_t &row : rawBoard)
        {
            for (const Square &square : row)
            {
                if (square.isMarked)
                {
                    std::cout << '*' << square.value << "* ";
                }
                else
                {
                    std::cout << ' ' << square.value << "  ";
                }
            }

            // newline after every row
            std::cout << '\n';
        }
        // extra newline after the end of the board
        std::cout << '\n';
    }

    bool Board::isSolved() const
    {
        if (checkRows() || checkColumns())
        {
            return true;
        }
        return false;
    }

    bool Board::checkRows() const
    {
        for (const rowColumn_t &row : rawBoard)
        {
            bool rowComplete { true };
            for (const Square &square : row)
            {
                if (!square.isMarked)
                {
                    rowComplete = false;
                }
            }
            if (rowComplete)
            {
                return true;
            }
        }
        // if no complete rows were found
        return false;
    }

    bool Board::checkColumns() const
    {
        for (std::size_t col { 0 }; col < rawBoard.size(); ++col)
        {
            bool columnComplete { true };
            for (const rowColumn_t &row : rawBoard)
            {
                if (!row[col].isMarked)
                {
                    columnComplete = false;
                }
            }
            if (columnComplete)
            {
                return true;
            }
        }
        // if no complete columns were found
        return false;
    }

    void Board::mark(int value)
    {
        for (rowColumn_t &row : rawBoard)
        {
            for (Square &square : row)
            {
                if (square.value == value)
                {
                    square.isMarked = true;
                }
            }
        }
    }

    void Board::finish()
    {
        finished = true;
    }

    bool Board::isFinished() const
    {
        return finished;
    }

    int Board::sumUnmarked()
    {
        int sum { 0 };
        for (rowColumn_t &row : rawBoard)
        {
            for (Square &square : row)
            {
                if (!square.isMarked)
                {
                    sum += square.value;
                }
            }
        }
        return sum;
    }

}

int main()
{
    std::ifstream ifs { "input.txt" };
    std::string strInput;
    std::getline(ifs, strInput);
    // stringstream makes it easy to read integers from the guesses
    std::stringstream guesses { strInput };

    std::vector<std::unique_ptr<bingo::Board>> boards {};
    // there are a hundred boards so let's save some time
    boards.reserve(100);
    std::string dummy;
    while (ifs)
    {
        boards.push_back(std::unique_ptr<bingo::Board>
            { new bingo::Board {ifs } });
        ifs.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::getline(ifs, dummy);
    }

    int part1 { -1 };
    int part2 { -1 };
    while (guesses)
    {
        int value;
        char dummyComma;
        guesses >> value;
        guesses >> dummyComma;

        for (const std::unique_ptr<bingo::Board> &board : boards)
        {
            board->mark(value);
            if (board->isSolved())
            {
                // only if we did not already find the winning board
                if (part1 == -1)
                {
                    part1 = board->sumUnmarked() * value;
                }

                if (!board->isFinished())
                {
                    // part2 will end up as the score of the last board solved
                    part2 = board->sumUnmarked() * value;
                    // so that we do not count it twice
                    board->finish();
                }
            }
        }
    }

    std::cout << "Part 1: " << part1 << '\n';
    std::cout << "Part 2: " << part2 << '\n';
    return 0;
}
