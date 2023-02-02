import math


def check_prime(number: int):
    """Check if a number is prime.

    Args:
        number (int): Number to check.

    Returns:
        bool: True if the number is prime, False otherwise.
    """
    sqrt_number = math.sqrt(number)
    for i in range(2, int(sqrt_number) + 1):
        if (number / i).is_integer():
            return False
    return True


if __name__ == "__main__":
    print(f"check_prime(10,000,000) = {check_prime(10_000_000)}")
    print(f"check_prime(10,000,019) = {check_prime(10_000_019)}")
