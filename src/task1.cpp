#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cstdlib>

#define N 1000
#define WORKLOAD 200000
#define SAFETY_FACTOR 1.2

long long task1() {
    volatile long long result = 0;

    for (int i = 0; i < WORKLOAD; i++) {
        long long a = rand() % 100000;
        long long b = rand() % 100000;
        result += a * b;
    }

    return result;
}

double percentile(const std::vector<double>& data, double p) {
    double index = p * (data.size() - 1);
    int lower = (int)index;
    int upper = lower + 1;

    if (upper >= (int)data.size()) {
        return data[lower];
    }

    double weight = index - lower;
    return data[lower] * (1 - weight) + data[upper] * weight;
}

int main() {
    std::vector<double> times;
    times.reserve(N);

    srand(0);

    for (int i = 0; i < N; i++) {
        auto start = std::chrono::high_resolution_clock::now();

        volatile long long result = task1();

        auto end = std::chrono::high_resolution_clock::now();

        auto duration_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();

        double duration_seconds = duration_ns / 1000000000.0;
        times.push_back(duration_seconds);
    }

    std::sort(times.begin(), times.end());

    double minimum = times.front();
    double q1 = percentile(times, 0.25);
    double q2 = percentile(times, 0.50);
    double q3 = percentile(times, 0.75);
    double maximum = times.back();
    double wcet = maximum * SAFETY_FACTOR;

    std::cout << "Number of measurements: " << N << std::endl;
    std::cout << "Min: " << minimum << " s" << std::endl;
    std::cout << "Q1: " << q1 << " s" << std::endl;
    std::cout << "Median Q2: " << q2 << " s" << std::endl;
    std::cout << "Q3: " << q3 << " s" << std::endl;
    std::cout << "Max: " << maximum << " s" << std::endl;
    std::cout << wcet << std::endl;

    return 0;
}