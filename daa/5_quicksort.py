def quicksort(arr):
    """
    QuickSort algorithm - sorts array in ascending order
    Time Complexity: O(n log n) average, O(n²) worst case
    Space Complexity: O(log n) due to recursion
    """
    if len(arr) <= 1:
        return arr
    
    # Choose pivot (middle element)
    pivot = arr[len(arr) // 2]
    
    # Partition into three lists
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Recursively sort and combine
    return quicksort(left) + middle + quicksort(right)


def quicksort_inplace(arr, low=0, high=None):
    """
    In-place QuickSort using Lomuto partition scheme
    More memory efficient - sorts the array directly
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition and get pivot index
        pivot_idx = partition(arr, low, high)
        
        # Recursively sort left and right subarrays
        quicksort_inplace(arr, low, pivot_idx - 1)
        quicksort_inplace(arr, pivot_idx + 1, high)
    
    return arr


def partition(arr, low, high):
    """
    Lomuto partition scheme
    Places pivot in correct position and returns its index
    """
    pivot = arr[high]  # Choose last element as pivot
    i = low - 1  # Index of smaller element
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap
    
    # Place pivot in correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Example usage and comparison
if __name__ == "__main__":
    # Test data
    arr1 = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
    arr2 = arr1.copy()
    
    print("Original array:")
    print(arr1)
    
    print("\n--- Using Simple QuickSort (creates new arrays) ---")
    sorted1 = quicksort(arr1)
    print("Sorted array:", sorted1)
    
    print("\n--- Using In-Place QuickSort (modifies original) ---")
    quicksort_inplace(arr2)
    print("Sorted array:", arr2)
    
    # Test with edge cases
    print("\n--- Edge Cases ---")
    print("Empty array:", quicksort([]))
    print("Single element:", quicksort([5]))
    print("Already sorted:", quicksort([1, 2, 3, 4, 5]))
    print("Reverse sorted:", quicksort([5, 4, 3, 2, 1]))
    print("Duplicates:", quicksort([3, 1, 4, 1, 5, 9, 2, 6, 5]))
    
    # Performance test
    import random
    import time
    
    large_arr = [random.randint(1, 1000) for _ in range(1000)]
    
    start = time.time()
    quicksort(large_arr.copy())
    end = time.time()
    print(f"\nTime for 1000 elements: {(end - start) * 1000:.2f} ms")