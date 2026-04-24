#include <iostream>
#include <cstdlib>

#define WORKLOAD 200000

int main() {
    volatile long long result = 0;

    for (int i = 0; i < WORKLOAD; i++) {
        long long a = rand() % 100000;
        long long b = rand() % 100000;
        result += a * b;
    }

    std::cout << result << std::endl;
    return 0;
}