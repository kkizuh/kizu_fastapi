import requests
import random
import datetime

API_URL = "http://213.108.22.26:8000"  # или твой внешний адрес
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrcmlzIiwiaWQiOjEsImV4cCI6MTc0ODc5Nzk1N30.k2ag162vngC24hqepSQsD0RMh1Z94BPtX_e2ALjJHfM"  # вставь сюда токен

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

DEFAULT_CATEGORIES = {
    "income": ["Зарплата", "Фриланс", "Кэшбэк"],
    "expense": ["Еда", "Транспорт", "Подписка", "Развлечения", "Аптека"]
}

TITLES = {
    "income": ["Зарплата", "Фриланс", "Кэшбэк"],
    "expense": ["Еда", "Транспорт", "Подписка", "Развлечения", "Аптека"]
}


def ensure_categories():
    # Получить список категорий
    r = requests.get(f"{API_URL}/categories", headers=HEADERS)
    r.raise_for_status()
    existing = r.json()

    result = {"income": [], "expense": []}
    for t in ("income", "expense"):
        for name in DEFAULT_CATEGORIES[t]:
            # Найдена ли такая категория?
            match = next((c for c in existing if c["name"] == name and c["type"] == t), None)
            if match:
                result[t].append(match["id"])
            else:
                # Создать новую категорию
                r = requests.post(
                    f"{API_URL}/categories",
                    headers=HEADERS,
                    json={"name": name, "type": t}
                )
                r.raise_for_status()
                new_cat = r.json()
                result[t].append(new_cat["id"])
                print(f"[+] Создана категория {name} ({t})")

    return result


def create_transaction(tr_type: str, category_ids: list):
    title = random.choice(TITLES[tr_type])
    amount = round(random.uniform(100, 2000), 2)
    date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))
    date_str = date.isoformat()

    payload = {
        "title": title,
        "amount": amount,
        "transaction_type": tr_type,
        "category_ids": [random.choice(category_ids)],
        "date": date_str
    }

    r = requests.post(f"{API_URL}/transactions", json=payload, headers=HEADERS)
    if r.status_code == 200:
        print(f"[✔] {tr_type.title()} - {title} на {amount} ₽")
    else:
        print(f"[✘] Ошибка: {r.status_code} - {r.text}")


if __name__ == "__main__":
    categories = ensure_categories()
    for _ in range(10):
        create_transaction("income", categories["income"])
    for _ in range(20):
        create_transaction("expense", categories["expense"])