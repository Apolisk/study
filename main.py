import random

url_mapping = {}
BASE_URL = "https://"

nouns = ["fast", "evil"]

adjectives = ["tiger", "cat"]

users = {
    1:{},
    2:{}
}

def read_url() -> str:
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return f"{BASE_URL}{noun}-{adjective}"

def decrease_url(user_id: int, long_url: str) -> str:
    if long_url in users[user_id]:
        return users[user_id][long_url]
    short_url = read_url()
    users[user_id][short_url] = long_url
    print(users)
    return short_url

def expand_url(user_id: int, short_url: str) -> str:
    long_url = users[user_id].get(short_url)
    if long_url is None:
        return "Error: short link does not exist"
    return long_url

def login(user_id: int):
    if user_id not in users:
        print("Invalid user id")
    else:
        option = int(input(f"User {user_id} already logged in\n1 - decrease url\n 2 - expand url\n3 - login menu\nChoose option: "))
        if  option == 1:
            long_url = input("Long url: ")
            print(f"Short url: {decrease_url(user_id, long_url)}")
        elif  option == 2:
            short_url = input("Short url: ")
            print(f"Long url is: {expand_url(user_id, short_url)}")

while True:
    try:
        user_id = int(input("Введите ваш ID для входа (1 или 2): "))
        login(user_id)
    except ValueError:
        print("Ошибка: введите корректный ID.")