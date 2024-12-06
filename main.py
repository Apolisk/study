import random
from typing import Optional


BASE_URL = "https://"
MAX_ATTEMPTS = 10

nouns = ["fast", "evil"]
adjectives = ["tiger", "cat"]

users = {
    1: {},
    2: {}
}


def read_url() -> str:
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return f"{BASE_URL}{noun}-{adjective}"


def decrease_url(user_id: int, long_url: str) -> Optional[str]:
    for attempt in range(MAX_ATTEMPTS):
        short_url = read_url()
        print(short_url)
        if short_url not in users[user_id]:
            users[user_id][short_url] = long_url
            return short_url
    return None

def expand_url(user_id: int, short_url: str) -> Optional[str]:
    long_url = users[user_id].get(short_url)
    return long_url


def login(user_id: int) -> int:
    return user_id in users


def menu(user_id: int):
    option = int(input(
        f"User {user_id} already logged in\n"
        f"1 - decrease url\n"
        f"2 - expand url\n"
        f"3 - login menu\n"
        f"Choose option: "
    ))
    if option == 1:
        long_url = input("Long url: ")
        result = decrease_url(user_id, long_url)
        if result is None:
            print("Can`t save url")
        else:
            print(f"Short url: {result}")
    elif option == 2:
        short_url = input("Short url: ")
        result = expand_url(user_id, short_url)
        if result is None:
            print("No long url saved")
        else:
            print(f"Long url is: {result}")


while True:
    try:
        user_id = int(input("Enter your ID to log in: "))
        exists = login(user_id)
        if exists:
            menu(user_id)
    except ValueError:
        print("Error. Enter correct ID.")
