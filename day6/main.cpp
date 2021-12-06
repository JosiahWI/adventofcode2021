#include <fstream>
#include <iostream>

// I learned the right way to solve this afterwards, but this is my
// original naive solution.

long simulateFish(int startTime, int days)
{
    days -= startTime;
    long long total { 0 };
    for (int d { 0 }; days >= 0; days -= 7)
    {
        total += 1 + simulateFish(9, days);
    }
    return total;
}

int main()
{
    std::ifstream ifs { "input.txt" };
    
    long long totalFish { 0 };
    while (ifs)
    {
        int startTime;
        ifs >> startTime;
        char dummyComma;
        ifs >> dummyComma;
        totalFish += 1 + simulateFish(startTime + 1, 256);
        std::cout << totalFish << '\n';
    }
    std::cout << totalFish << '\n';
    return 0;
}
