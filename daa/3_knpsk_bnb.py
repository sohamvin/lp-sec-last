from queue import Queue
from dataclasses import dataclass
from typing import List

@dataclass
class Item:
    """Represents an item with weight, value, and value-to-weight ratio"""
    weight: int
    value: int
    ratio: float = 0.0
    
    def __post_init__(self):
        self.ratio = self.value / self.weight if self.weight > 0 else 0


@dataclass
class Node:
    """Represents a node in the search tree"""
    level: int      # Current item being considered
    profit: int     # Total profit so far
    weight: int     # Total weight so far
    bound: float    # Upper bound on maximum profit possible from this node
    items_taken: List[int] = None  # Track which items are taken
    
    def __post_init__(self):
        if self.items_taken is None:
            self.items_taken = []


def calculate_bound(node, n, capacity, items):
    """
    Calculate the upper bound of profit that can be achieved from this node.
    Uses fractional knapsack for remaining items (greedy approach).
    """
    # If weight exceeds capacity, no profit possible
    if node.weight >= capacity:
        return 0
    
    profit_bound = node.profit
    j = node.level + 1
    total_weight = node.weight
    
    # Greedily add items while they fit completely
    while j < n and total_weight + items[j].weight <= capacity:
        total_weight += items[j].weight
        profit_bound += items[j].value
        j += 1
    
    # Add fraction of next item if there's remaining capacity
    if j < n:
        remaining_capacity = capacity - total_weight
        profit_bound += remaining_capacity * items[j].ratio
    
    return profit_bound


def knapsack_branch_and_bound(capacity, items):
    """
    Solves 0/1 Knapsack using Branch and Bound algorithm.
    
    Strategy:
    1. Sort items by value-to-weight ratio (descending)
    2. Explore search tree using BFS
    3. For each node, create two children:
       - Include current item
       - Exclude current item
    4. Prune branches where bound <= current max profit
    
    Time Complexity: O(2^n) worst case, but pruning makes it faster in practice
    Space Complexity: O(n) for queue
    """
    n = len(items)
    
    # Sort items by value-to-weight ratio in descending order
    items.sort(key=lambda x: x.ratio, reverse=True)
    
    # Initialize queue with root node
    Q = Queue()
    root = Node(level=-1, profit=0, weight=0, bound=0, items_taken=[])
    Q.put(root)
    
    max_profit = 0
    best_items = []
    nodes_explored = 0
    nodes_pruned = 0
    
    while not Q.empty():
        u = Q.get()
        nodes_explored += 1
        
        # If this is root node, start with first item
        if u.level == -1:
            v_level = 0
        else:
            v_level = u.level + 1
        
        # If we've considered all items, skip
        if v_level >= n:
            continue
        
        # === Option 1: INCLUDE the current item ===
        v_include = Node(
            level=v_level,
            weight=u.weight + items[v_level].weight,
            profit=u.profit + items[v_level].value,
            bound=0,
            items_taken=u.items_taken + [v_level]
        )
        
        # If this node is feasible and better than current max
        if v_include.weight <= capacity and v_include.profit > max_profit:
            max_profit = v_include.profit
            best_items = v_include.items_taken.copy()
        
        # Calculate bound and add to queue if promising
        v_include.bound = calculate_bound(v_include, n, capacity, items)
        if v_include.bound > max_profit:
            Q.put(v_include)
        else:
            nodes_pruned += 1
        
        # === Option 2: EXCLUDE the current item ===
        v_exclude = Node(
            level=v_level,
            weight=u.weight,
            profit=u.profit,
            bound=0,
            items_taken=u.items_taken.copy()
        )
        
        # Calculate bound and add to queue if promising
        v_exclude.bound = calculate_bound(v_exclude, n, capacity, items)
        if v_exclude.bound > max_profit:
            Q.put(v_exclude)
        else:
            nodes_pruned += 1
    
    return max_profit, best_items, nodes_explored, nodes_pruned


def knapsack_bnb_verbose(capacity, items_data):
    """
    Wrapper function with detailed output
    """
    # Create Item objects
    items = [Item(w, v) for w, v in items_data]
    
    print("=== Branch and Bound Knapsack ===")
    print(f"Capacity: {capacity}\n")
    
    print("Original Items:")
    for i, item in enumerate(items):
        print(f"  Item {i}: weight={item.weight}, value={item.value}, ratio={item.ratio:.2f}")
    
    # Solve
    max_profit, selected_indices, nodes_explored, nodes_pruned = knapsack_branch_and_bound(capacity, items)
    
    # Items are sorted by ratio in the algorithm, so we need to track original indices
    items_sorted = sorted(enumerate(items), key=lambda x: x[1].ratio, reverse=True)
    
    print("\n" + "="*50)
    print(f"✓ Maximum Profit: {max_profit}")
    print(f"✓ Nodes Explored: {nodes_explored}")
    print(f"✓ Nodes Pruned: {nodes_pruned}")
    print(f"✓ Efficiency: {nodes_pruned}/{nodes_explored + nodes_pruned} nodes saved")
    
    if selected_indices:
        print("\nSelected Items (after sorting by ratio):")
        total_weight = 0
        total_value = 0
        for idx in selected_indices:
            orig_idx, item = items_sorted[idx]
            total_weight += item.weight
            total_value += item.value
            print(f"  Original Item {orig_idx}: weight={item.weight}, value={item.value}")
        print(f"\nTotal Weight: {total_weight}/{capacity}")
        print(f"Total Value: {total_value}")
    
    return max_profit


# Example usage
if __name__ == "__main__":
    # Test case 1: Simple example from C++ code
    print("TEST CASE 1")
    print("-" * 50)
    capacity1 = 50
    items1 = [(10, 60), (20, 100), (30, 120)]
    result1 = knapsack_bnb_verbose(capacity1, items1)
    
    print("\n\n" + "="*70 + "\n")
    
    # Test case 2: Larger example
    print("TEST CASE 2")
    print("-" * 50)
    capacity2 = 269
    items2 = [
        (95, 55), (4, 10), (60, 47), (32, 5), (23, 4),
        (72, 50), (80, 8), (62, 61), (65, 85), (46, 87)
    ]
    result2 = knapsack_bnb_verbose(capacity2, items2)
    
    print("\n\n" + "="*70 + "\n")
    
    # Comparison with DP approach
    print("KEY DIFFERENCES: Branch & Bound vs Dynamic Programming")
    print("-" * 50)
    print("Branch & Bound:")
    print("  ✓ Uses intelligent search tree exploration")
    print("  ✓ Prunes unpromising branches (reduces search space)")
    print("  ✓ Better for large capacity, fewer items")
    print("  ✓ Can find solutions without exploring all possibilities")
    print("\nDynamic Programming:")
    print("  ✓ Guarantees to check all subproblems")
    print("  ✓ Better for smaller capacity values")
    print("  ✓ Time: O(n*W), Space: O(n*W)")