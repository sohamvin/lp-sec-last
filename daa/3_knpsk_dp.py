def knapsack_dp(capacity, weights, values):
    """
    Solves the 0/1 Knapsack problem using Dynamic Programming
    
    Args:
        capacity: Maximum weight the knapsack can hold
        weights: List of item weights
        values: List of item values
    
    Returns:
        Maximum value that can be obtained
    """
    n = len(weights)
    
    # Create a 2D DP table: dp[i][w] = max value using first i items with capacity w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Build the DP table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # Current item index (0-based)
            item_weight = weights[i - 1]
            item_value = values[i - 1]
            
            # If current item can fit in the knapsack
            if item_weight <= w:
                # Choose maximum of:
                # 1. Don't include item: dp[i-1][w]
                # 2. Include item: dp[i-1][w-weight] + value
                dp[i][w] = max(
                    dp[i - 1][w],  # Don't take item
                    dp[i - 1][w - item_weight] + item_value  # Take item
                )
            else:
                # Item too heavy, can't include it
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]


def knapsack_with_items(capacity, weights, values):
    """
    Returns both maximum value AND which items to include
    """
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Build DP table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            item_weight = weights[i - 1]
            item_value = values[i - 1]
            
            if item_weight <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - item_weight] + item_value
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    # Backtrack to find which items were selected
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        # If value changed, this item was included
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)  # 0-based index
            w -= weights[i - 1]
    
    selected_items.reverse()
    return dp[n][capacity], selected_items


def knapsack_space_optimized(capacity, weights, values):
    """
    Space-optimized version using only O(W) space instead of O(n*W)
    """
    n = len(weights)
    # Only need current and previous row
    prev = [0] * (capacity + 1)
    
    for i in range(n):
        curr = [0] * (capacity + 1)
        for w in range(1, capacity + 1):
            if weights[i] <= w:
                curr[w] = max(prev[w], prev[w - weights[i]] + values[i])
            else:
                curr[w] = prev[w]
        prev = curr
    
    return prev[capacity]


# Example usage
if __name__ == "__main__":
    # Example from the C++ code
    capacity = 269
    items = [
        (95, 55), (4, 10), (60, 47), (32, 5), (23, 4),
        (72, 50), (80, 8), (62, 61), (65, 85), (46, 87)
    ]
    
    weights = [item[0] for item in items]
    values = [item[1] for item in items]
    
    print("=== 0/1 Knapsack Problem ===")
    print(f"Knapsack Capacity: {capacity}")
    print(f"Number of items: {len(items)}")
    print("\nItems (weight, value):")
    for i, (w, v) in enumerate(items):
        print(f"  Item {i}: weight={w}, value={v}")
    
    # Method 1: Basic DP
    max_value = knapsack_dp(capacity, weights, values)
    print(f"\n✓ Maximum value: {max_value}")
    
    # Method 2: With item tracking
    max_value, selected = knapsack_with_items(capacity, weights, values)
    print(f"\n✓ Selected items (indices): {selected}")
    print("Selected items details:")
    total_weight = 0
    total_value = 0
    for idx in selected:
        w, v = items[idx]
        total_weight += w
        total_value += v
        print(f"  Item {idx}: weight={w}, value={v}")
    print(f"Total weight: {total_weight}/{capacity}")
    print(f"Total value: {total_value}")
    
    # Method 3: Space optimized
    max_value_opt = knapsack_space_optimized(capacity, weights, values)
    print(f"\n✓ Space-optimized result: {max_value_opt}")
    
    # Additional test case
    print("\n=== Simple Test Case ===")
    test_capacity = 50
    test_weights = [10, 20, 30]
    test_values = [60, 100, 120]
    result = knapsack_dp(test_capacity, test_weights, test_values)
    print(f"Capacity: {test_capacity}")
    print(f"Items: {list(zip(test_weights, test_values))}")
    print(f"Maximum value: {result}")