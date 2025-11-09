#include <bits/stdc++.h>
using namespace std;

struct Item {
  int weight;
  int value;
};

// Function to solve the knapsack problem using dynamic programming
int knapsack(int W, vector<Item> &items) {
  int n = items.size();
  vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));

  for (int i = 1; i <= n; i++) {
    // Iterate over each capacity from 1 to W
    for (int w = 1; w <= W; w++) {
      // If the current item's weight is less than or equal to the current
      // capacity
      if (items[i - 1].weight <= w) {
        // Take the maximum of not including the item or including the item
        dp[i][w] = max(dp[i - 1][w],
                       dp[i - 1][w - items[i - 1].weight] + items[i - 1].value);
      } else {
        // current item's weight is more than the current capacity, skip
        dp[i][w] = dp[i - 1][w];
      }
    }
  }

  // The maximum value that can be obtained with the given capacity W
  return dp[n][W];
}

int main() {
  int W = 269; // Knapsack capacity
  vector<Item> items = {{95, 55}, {4, 10},  {60, 47}, {32, 5},
                        {23, 4},  {72, 50}, {80, 8},  {62, 61},
                        {65, 85}, {46, 87}}; // {weight, value}

  int max_value = knapsack(W, items);
  cout << "Maximum value: " << max_value << endl;

  return 0;
}