"""
HW08 Task 2: Sliding Window Rate Limiter (50 points)

Problem: Implement a rate limiter for a chat application that controls
how many messages a user can send within a specific time window using
the Sliding Window algorithm.

Configuration (as per assignment):
- Window size: 10 seconds
- Maximum messages per window: 1 message per user

Sliding Window vs Fixed Window:
- Fixed Window: Divides time into fixed intervals, resets at boundaries
  Problem: User can send at t=9s and t=11s (2 messages in 2 seconds)

- Sliding Window: Window "slides" with current time
  At t=11s, window is [1s - 11s], so message at t=9s still counts
  More accurate rate limiting

Acceptance Criteria:
- can_send_message(user_id) correctly checks rate limits (15 pts)
- record_message(user_id) properly logs timestamps (15 pts)
- time_until_next_allowed(user_id) returns accurate wait time (10 pts)
- Uses defaultdict(list) as specified (5 pts)
- Edge cases handled (empty window, multiple users) (5 pts)
"""

import time
from collections import defaultdict
from typing import Dict, List


class SlidingWindowRateLimiter:
    """
    Rate limiter using Sliding Window algorithm.

    Controls message frequency per user within a sliding time window.
    The window "slides" with time - old messages automatically become
    irrelevant as time passes.

    How it works:
    - Each user has a list of message timestamps
    - Window spans from (current_time - window_size) to current_time
    - Only timestamps within the window are counted
    - If count < max_messages, user can send
    """

    def __init__(self, window_size: float = 10.0, max_messages: int = 1):
        """
        Initialize rate limiter.

        Args:
            window_size: Time window in seconds (default: 10.0)
            max_messages: Maximum messages allowed per window (default: 1)

        Example:
            limiter = SlidingWindowRateLimiter(window_size=10.0, max_messages=1)
        """
        self.window_size = window_size
        self.max_messages = max_messages
        # TODO: Initialize user_messages using defaultdict(list)
        # Each user_id maps to a list of timestamps
        self.user_messages = defaultdict(list)


    def _clean_old_messages(self, user_id: str, current_time: float) -> None:
        """
        Remove messages outside the current sliding window.

        Called before any operation to ensure only relevant timestamps
        are considered.

        Args:
            user_id: The user identifier
            current_time: Current timestamp (from time.time())

        Algorithm:
            1. Calculate cutoff time: current_time - window_size
            2. Keep only timestamps > cutoff_time
        """
        # TODO: Calculate cutoff time
        cutoff_time = current_time - self.window_size

        # TODO: Filter to keep only messages within window
        self.user_messages[user_id] = [
            timestamp for timestamp in self.user_messages[user_id]
            if timestamp > cutoff_time
        ]

    def can_send_message(self, user_id: str) -> bool:
        """
        Check if user can send a message now.

        Cleans old messages first, then checks if user is under the limit.

        Args:
            user_id: The user identifier

        Returns:
            True if user can send (under rate limit), False otherwise

        Example:
            if limiter.can_send_message("user_1"):
                # User can send
                limiter.record_message("user_1")
            else:
                # User is rate limited
                wait = limiter.time_until_next_allowed("user_1")
        """
        # TODO: Get current time
        # TODO: Clean old messages for this user
        # TODO: Return True if message count < max_messages, else False
        current_time = time.time()
        self._clean_old_messages(user_id, current_time)
        return len(self.user_messages[user_id]) < self.max_messages

    def record_message(self, user_id: str) -> bool:
        """
        Record a message attempt for the user.

        Should only be called after can_send_message returns True.
        Records current timestamp in user's message list.

        Args:
            user_id: The user identifier

        Returns:
            True if message was recorded, False if rate limited

        Note: This method checks can_send_message first for safety,
        but in practice, caller should check first to avoid race conditions.
        """
        # TODO: Check if user can send (call can_send_message)
        # TODO: If rate limited, return False
        # TODO: Record current timestamp
        # TODO: Return True
        if not self.can_send_message(user_id):
            return False
        current_time = time.time()
        self.user_messages[user_id].append(current_time)
        return True

    def time_until_next_allowed(self, user_id: str) -> float:
        """
        Get time remaining until user can send next message.

        Calculates when the oldest message in the window will "slide out",
        making room for a new message.

        Args:
            user_id: The user identifier

        Returns:
            Seconds until next message allowed (0.0 if allowed now)

        Algorithm:
            1. Clean old messages
            2. If under limit, return 0.0 (can send now)
            3. Find oldest timestamp in window
            4. Calculate: (oldest + window_size) - current_time
            5. Return max(0.0, calculated_time)

        Example:
            wait = limiter.time_until_next_allowed("user_1")
            if wait > 0:
                print(f"Please wait {wait:.2f} seconds")
            else:
                print("You can send now")
        """
        # TODO: Get current time
        # TODO: Clean old messages
        # TODO: If under limit, return 0.0
        # TODO: Find oldest message timestamp
        # TODO: Calculate time until that message expires
        # TODO: Return max(0.0, time_remaining)
        current_time = time.time()
        self._clean_old_messages(user_id, current_time)

        if len(self.user_messages[user_id]) < self.max_messages:
            return 0.0

        # Find oldest message - it will be the first to expire
        oldest_timestamp = min(self.user_messages[user_id])
        time_remaining = (oldest_timestamp + self.window_size) - current_time
        return max(0.0, time_remaining)

    def get_message_count(self, user_id: str) -> int:
        """
        Get current message count for user in window.

        Args:
            user_id: The user identifier

        Returns:
            Number of messages in current sliding window
        """
        # TODO: Clean old messages
        # TODO: Return length of user's message list
        current_time = time.time()
        self._clean_old_messages(user_id, current_time)
        return len(self.user_messages[user_id])


def demonstrate_rate_limiter():
    """
    Demonstrate the sliding window rate limiter.

    Shows basic functionality without real time delays.
    """
    print("=" * 60)
    print("Sliding Window Rate Limiter Demonstration")
    print("=" * 60)
    print(f"Configuration: Window = 10 seconds, Max messages = 1")
    print()

    # TODO: Create rate limiter
    limiter = SlidingWindowRateLimiter(window_size=10.0, max_messages=1)

    # TODO: Test with multiple users
    users = ["user_1", "user_2"]

    print("--- Initial Test: First Message ---\n")

    for user_id in users:
        print(f"[{user_id}] Checking if can send message...")
        if limiter.can_send_message(user_id):
            print(f"[{user_id}] ✓ Can send message")
            success = limiter.record_message(user_id)
            if success:
                print(f"[{user_id}] Message recorded successfully")
        else:
            wait_time = limiter.time_until_next_allowed(user_id)
            print(f"[{user_id}] ✗ Rate limited. Wait {wait_time:.2f} seconds")

    print("\n--- Attempting Immediate Second Message ---\n")

    for user_id in users:
        if limiter.can_send_message(user_id):
            print(f"[{user_id}] ✓ Can send message")
        else:
            wait_time = limiter.time_until_next_allowed(user_id)
            print(f"[{user_id}] ✗ Rate limited. Wait {wait_time:.2f} seconds")

    print("\n--- Message Count Status ---\n")
    for user_id in users:
        count = limiter.get_message_count(user_id)
        print(f"[{user_id}] Messages in window: {count}/{limiter.max_messages}")


def interactive_test():
    """
    Interactive test with real timing delays.

    Uncomment and run to see actual sliding window behavior.
    Warning: Takes ~15 seconds to complete due to sleep() calls.
    """
    print("\n" + "=" * 60)
    print("Interactive Rate Limiter Test (with real delays)")
    print("=" * 60)

    # TODO: Uncomment for live testing
    limiter = SlidingWindowRateLimiter(window_size=10.0, max_messages=1)
    user_id = "test_user"

    # First message
    print(f"\n[T=0s] Attempting to send message...")
    if limiter.record_message(user_id):
        print("✓ Message sent successfully!")

    # Try immediately again
    print(f"\n[T=0s] Attempting second message immediately...")
    if limiter.can_send_message(user_id):
        print("✓ Can send")
    else:
        wait = limiter.time_until_next_allowed(user_id)
        print(f"✗ Rate limited. Must wait {wait:.2f} seconds")

    # Wait 5 seconds
    print("\n[Waiting 5 seconds...]")
    time.sleep(5)

    print(f"\n[T=5s] Attempting message...")
    if limiter.can_send_message(user_id):
        print("✓ Can send")
    else:
        wait = limiter.time_until_next_allowed(user_id)
        print(f"✗ Still rate limited. Wait {wait:.2f} more seconds")

    # Wait remaining time
    remaining = limiter.time_until_next_allowed(user_id)
    if remaining > 0:
        print(f"\n[Waiting {remaining:.1f} more seconds...]")
        time.sleep(remaining + 0.1)

    print(f"\n[T=10s+] Attempting message...")
    if limiter.record_message(user_id):
        print("✓ Message sent successfully! Window has reset.")


# ============== MAIN ==============

def main():
    """Main entry point."""
    demonstrate_rate_limiter()

    print("\n" + "=" * 60)
    print("Sliding Window Visualization")
    print("=" * 60)
    print("""
    Sliding Window (10s window, 1 msg max):

    Time: ----[=========WINDOW=========]---->
              |                        |
              now - 10s                now

    Example scenario:
    t=0s:  User sends message ✓ (window empty)
    t=3s:  User tries again  ✗ (1 msg in [0s-10s] window)
    t=8s:  User tries again  ✗ (1 msg in [0s-10s] window)
    t=10s: User can send     ✓ (original msg slides out)

    Key insight: The window SLIDES with time, not fixed boundaries.
    """)

    # Optional: Run interactive test
    interactive_test()


if __name__ == "__main__":
    main()
