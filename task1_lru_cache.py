"""
HW08 Task 1: LRU Cache for Optimizing Range Sum Queries (50 points)

Problem: Implement a caching system using LRU (Least Recently Used) Cache
to optimize range sum queries on a large array. Compare performance with
and without caching.

LRU Cache Properties:
- When cache is full, evicts the least recently used item
- Most recently accessed items are kept in cache
- O(1) get and put operations using OrderedDict
- Supports cache invalidation when underlying data changes

Test Data Requirements:
- Array of 100,000 random integers (range: 1-1000)
- 50,000 random queries as (L, R) pairs where L <= R

Acceptance Criteria:
- LRUCache class correctly implements LRU eviction policy (20 pts)
- range_sum_with_cache properly uses cache for optimization (20 pts)
- Performance comparison shows measurable improvement (10 pts)
"""

from collections import OrderedDict
import random
import time
from typing import List, Tuple, Any, Callable, Optional


class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation using OrderedDict.

    When capacity is reached, the least recently used item is evicted.
    OrderedDict maintains insertion order, and move_to_end() marks
    items as recently used.

    Key features:
    - O(1) get and put operations
    - Automatic eviction of LRU items
    - Support for cache invalidation via predicate function
    """

    def __init__(self, capacity: int):
        """
        Initialize LRU Cache with given capacity.

        Args:
            capacity: Maximum number of items to store

        Example:
            cache = LRUCache(capacity=1000)
        """
        self.capacity = capacity
        # TODO: Initialize OrderedDict for cache storage
        # self.cache = OrderedDict()
        self.cache = OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        """
        Retrieve value from cache.

        If key exists, moves it to end (marks as most recently used).

        Args:
            key: The cache key to look up

        Returns:
            Cached value if found, None otherwise

        Algorithm:
            1. If key not in cache, return None
            2. Move key to end (most recently used)
            3. Return cached value
        """
        # TODO: Check if key exists in cache
        # TODO: If not exists, return None
        # TODO: Move to end (mark as recently used)
        # TODO: Return the cached value
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> None:
        """
        Store value in cache.

        If key already exists, updates value and moves to end.
        If cache is full, removes least recently used item first.

        Args:
            key: Cache key
            value: Value to store

        Algorithm:
            1. If key exists, move to end
            2. Else if at capacity, remove oldest item (popitem(last=False))
            3. Store key-value pair
        """
        # TODO: If key already exists, move to end
        # TODO: Else check if at capacity, remove oldest if needed
        # TODO: Store key-value pair
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def __contains__(self, key: Any) -> bool:
        """Support 'in' operator for checking key existence."""
        # TODO: Return whether key is in cache
        return key in self.cache

    def __len__(self) -> int:
        """Return number of cached items."""
        # TODO: Return length of cache
        return len(self.cache)

    def invalidate(self, predicate: Callable[[Any], bool]) -> None:
        """
        Remove all cache entries matching a predicate function.

        Used when underlying data changes and some cached results
        become invalid.

        Args:
            predicate: Function that takes a key and returns True
                      if that key should be invalidated

        Example:
            # Invalidate all ranges that include index 5
            cache.invalidate(lambda key: key[0] <= 5 <= key[1])

        Algorithm:
            1. Find all keys where predicate returns True
            2. Delete those keys from cache
        """
        # TODO: Find all keys to remove (where predicate(key) is True)
        # keys_to_remove = [key for key in self.cache if predicate(key)]

        # TODO: Remove those keys
        # for key in keys_to_remove:
        #     del self.cache[key]
        keys_to_remove = [key for key in self.cache if predicate(key)]
        for key in keys_to_remove:
            del self.cache[key]


def range_sum_no_cache(array: List[int], L: int, R: int) -> int:
    """
    Calculate sum of array[L:R+1] without caching.

    Simple baseline implementation for performance comparison.

    Args:
        array: The input array
        L: Left index (inclusive)
        R: Right index (inclusive)

    Returns:
        Sum of elements from index L to R (inclusive)

    Complexity: O(R - L) per query
    """
    # TODO: Return sum of array slice from L to R+1
    return sum(array[L:R+1])


def range_sum_with_cache(array: List[int], L: int, R: int, cache: LRUCache) -> int:
    """
    Calculate sum of array[L:R+1] with LRU caching.

    Caches computed results to avoid recalculation for repeated queries.

    Args:
        array: The input array
        L: Left index (inclusive)
        R: Right index (inclusive)
        cache: LRUCache instance for storing results

    Returns:
        Sum of elements from index L to R (inclusive)

    Algorithm:
        1. Create unique key from (L, R)
        2. Check if result is in cache
        3. If cached, return cached value
        4. Otherwise compute, cache, and return result

    Complexity: O(1) for cache hit, O(R - L) for cache miss
    """
    # TODO: Create unique key for this query (tuple (L, R))
    # TODO: Check cache for existing result
    # TODO: If found, return cached result
    # TODO: Otherwise calculate sum
    # TODO: Store result in cache
    # TODO: Return result
    key = (L, R)
    cached_result = cache.get(key)
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R+1])
    cache.put(key, result)
    return result


def update_array(array: List[int], idx: int, value: int, cache: LRUCache) -> None:
    """
    Update an array element and invalidate affected cache entries.

    When an element changes, any cached range sum that includes
    that element's index becomes invalid.

    Args:
        array: The input array (modified in place)
        idx: Index of element to update
        value: New value for the element
        cache: LRUCache instance to invalidate

    Invalidation rule:
        A cached range (L, R) includes idx if: L <= idx <= R

    Example:
        update_array(arr, 5, 100, cache)
        # Invalidates all cached ranges (L, R) where L <= 5 <= R
    """
    # TODO: Update the array element
    # TODO: Invalidate all cache entries where L <= idx <= R
    # cache.invalidate(lambda key: key[0] <= idx <= key[1])
    array[idx] = value
    cache.invalidate(lambda key: key[0] <= idx <= key[1])


def generate_test_data(array_size: int = 100000,
                       num_queries: int = 50000) -> Tuple[List[int], List[Tuple[int, int]]]:
    """
    Generate random test data for performance comparison.

    Args:
        array_size: Size of the array to generate (default 100,000)
        num_queries: Number of (L, R) query pairs (default 50,000)

    Returns:
        Tuple of (array, queries) where:
        - array: List of random integers 1-1000
        - queries: List of (L, R) tuples where L <= R
    """
    # TODO: Generate array of random integers 1-1000
    # TODO: Generate random queries (L, R) where L <= R
    # TODO: Return (array, queries)
    array = [random.randint(1, 1000) for _ in range(array_size)]

    # Create a pool of unique queries, then sample with repetition
    # This simulates real-world scenarios where some queries are repeated
    unique_query_count = min(1000, num_queries // 10)  # ~10% unique queries
    unique_queries = []
    for _ in range(unique_query_count):
        a, b = random.randint(0, array_size - 1), random.randint(0, array_size - 1)
        unique_queries.append((min(a, b), max(a, b)))

    # Sample from the pool with replacement to create repeated queries
    queries = [random.choice(unique_queries) for _ in range(num_queries)]
    return array, queries


def compare_performance(array: List[int],
                        queries: List[Tuple[int, int]],
                        cache_capacity: int = 1000) -> None:
    """
    Compare range sum performance with and without caching.

    Runs all queries using both methods and displays timing comparison.

    Args:
        array: The input array
        queries: List of (L, R) query pairs
        cache_capacity: Maximum cache size (default 1000)
    """
    # ===== Test without cache =====
    # TODO: Record start time
    # TODO: Execute all queries using range_sum_no_cache
    # TODO: Store results for verification
    # TODO: Record total time
    start_time = time.time()
    results_no_cache = [range_sum_no_cache(array, L, R) for L, R in queries]
    time_no_cache = time.time() - start_time
    # ===== Test with cache =====
    # TODO: Create LRUCache with given capacity
    # TODO: Record start time
    # TODO: Execute all queries using range_sum_with_cache
    # TODO: Store results for verification
    # TODO: Record total time
    start_time = time.time()
    cache = LRUCache(capacity=cache_capacity)
    results_with_cache = [range_sum_with_cache(array, L, R, cache) for L, R in queries]
    time_with_cache = time.time() - start_time
    # ===== Display results =====
    # TODO: Print formatted comparison table
    print(f"{'Method':<25} {'Time (seconds)':<15}")
    print("-" * 40)
    print(f"{'Without cache':<25} {time_no_cache:<15.4f}")
    print(f"{'With LRU cache':<25} {time_with_cache:<15.4f}")

    # TODO: Calculate and print speedup factor
    print(f"Speedup: {time_no_cache / time_with_cache:.2f}x")
    print(f"Cache entries: {len(cache)}")

    # TODO: Verify correctness (both methods produce same results)
    assert results_no_cache == results_with_cache, "Results mismatch!"
    print("✓ Results verified: Both methods produce identical results")


# ============== MAIN ==============

def main():
    """Main entry point for LRU Cache demonstration."""
    print("=" * 60)
    print("TASK 1: LRU Cache Performance Comparison")
    print("=" * 60)

    # Generate test data
    print("\nGenerating test data...")
    print("  - Array size: 100,000 elements")
    print("  - Number of queries: 50,000")

    # TODO: Uncomment when implementation is complete
    array, queries = generate_test_data(100000, 50000)

    # Compare with different cache sizes
    print("\nRunning performance comparison...")
    for cache_size in [100, 500, 1000, 5000]:
        print(f"\n--- Cache Capacity: {cache_size} ---")
        compare_performance(array, queries, cache_size)

    # Placeholder output
    print("\n" + "=" * 60)
    print("Expected Output Format:")
    print("=" * 60)
    print("""
    --- Cache Capacity: 1000 ---
    Method                    Time (seconds)
    ----------------------------------------
    Without cache             2.3456
    With LRU cache            1.8765
    ----------------------------------------
    Cache hits: 1000 unique queries cached
    Speedup: 1.25x

    ✓ Results verified: Both methods produce identical results
    """)


    # Additional demonstration: Cache invalidation
    print("\n" + "=" * 60)
    print("Cache Invalidation Demo:")
    print("=" * 60)
    print("""
    When array elements change, cached range sums become invalid.

    Example:
        array = [1, 2, 3, 4, 5]
        cache contains: {(0,2): 6, (1,3): 9, (2,4): 12}

        update_array(array, 2, 100, cache)  # Change index 2 from 3 to 100

        After invalidation:
        - (0,2) removed (includes index 2)
        - (1,3) removed (includes index 2)
        - (2,4) removed (includes index 2)

    This ensures cache never returns stale data.
    """)


if __name__ == "__main__":
    main()
