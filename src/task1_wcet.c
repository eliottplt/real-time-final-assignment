#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000
#define WORKLOAD 1000000

long long multiply_random_numbers() {
    volatile long long result = 0;

    for (int i = 0; i < WORKLOAD; i++) {
        long long a = rand() % 100000;
        long long b = rand() % 100000;
        result += a * b;
    }

    return result;
}

int main() {
    struct timespec start, end;
    double execution_time;

    srand(time(NULL));

    for (int i = 0; i < N; i++) {
        clock_gettime(CLOCK_MONOTONIC, &start);

        volatile long long result = multiply_random_numbers();

        clock_gettime(CLOCK_MONOTONIC, &end);

        execution_time =
            (end.tv_sec - start.tv_sec)
            + (end.tv_nsec - start.tv_nsec) / 1000000000.0;

        printf("%.9f\n", execution_time);
    }

    return 0;
}