#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

struct Item {
  int weight;
  int value;
  double ratio; // value per unit weight
};

struct Node {
  int level;
  int profit;
  int weight;
  double bound;
};

bool compareItems(Item a, Item b) { return a.ratio > b.ratio; }

double bound(Node u, int n, int W, vector<Item> &items) {
  if (u.weight >= W)
    return 0;
  double profit_bound = u.profit;
  int j = u.level + 1;
  int totweight = u.weight;

  while ((j < n) && (totweight + items[j].weight <= W)) {
    totweight += items[j].weight;
    profit_bound += items[j].value;
    j++;
  }

  if (j < n)
    profit_bound += (W - totweight) * items[j].ratio;

  return profit_bound;
}

int knapsack(int W, vector<Item> &items) {
  int n = items.size();
  sort(items.begin(), items.end(), compareItems);

  queue<Node> Q;
  Node u, v;
  u = {-1, 0, 0, 0};
  Q.push(u);

  int maxProfit = 0;

  while (!Q.empty()) {
    u = Q.front();
    Q.pop();

    if (u.level == -1)
      v.level = 0;

    if (u.level == n - 1)
      continue;

    v.level = u.level + 1;

    v.weight = u.weight + items[v.level].weight;
    v.profit = u.profit + items[v.level].value;

    if (v.weight <= W && v.profit > maxProfit)
      maxProfit = v.profit;

    v.bound = bound(v, n, W, items);

    if (v.bound > maxProfit)
      Q.push(v);

    v.weight = u.weight;
    v.profit = u.profit;
    v.bound = bound(v, n, W, items);

    if (v.bound > maxProfit)
      Q.push(v);
  }

  return maxProfit;
}

int main() {
  int W = 50; // Knapsack capacity
  vector<Item> items = {
      {10, 60, 6}, {20, 100, 5}, {30, 120, 4}}; // {weight, value, ratio}

  for (auto &item : items) {
    item.ratio = static_cast<double>(item.value) / item.weight;
  }

  int max_value = knapsack(W, items);
  cout << "Maximum value: " << max_value << endl;

  return 0;
}