import random

url_mapping = {}
BASE_URL = "https://"

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


def decrease_url(user_id: int, long_url: str) -> str:
    short_url = read_url()
    if short_url in users[user_id]:
        return users[user_id][short_url]
    users[user_id][short_url] = long_url
    return short_url


def expand_url(user_id: int, short_url: str) -> str:
    long_url = users[user_id].get(short_url)
    if long_url is None:
        return None
    return long_url


def login(user_id: int) -> int:
    if user_id not in users:
        return False
    return True


def menu(user_id: int):
    option = int(input(f"User {user_id} already logged in\n"
                           f"1 - decrease url\n"
                           f"2 - expand url\n"
                           f"3 - login menu\n"
                           f"Choose option: "))
    if option == 1:
        long_url = input("Long url: ")
        result = decrease_url(user_id, long_url)
        if result is None:
            print("No long url")
        else:
            print(f"Short url: {result}")
    elif option == 2:
        short_url = input("Short url: ")
        result = expand_url(user_id, short_url)
        if result is None:
            print("No long url")
        else:
            print(f"Long url is: {result}")


while True:
    try:
        user_id = int(input("Введите ваш ID для входа (1 или 2): "))
        exists = login(user_id)
        if exists:
            menu(user_id)
    except ValueError:
        print("Ошибка: введите корректный ID.")
