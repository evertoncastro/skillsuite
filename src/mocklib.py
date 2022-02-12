from random import randint


def update_user(user_data: dict):
    # Mock implementation of the library with random result
    print(f'User data received {user_data}')
    return 'success' if (randint(0, 9) % 2) == 0 else 'fail'
