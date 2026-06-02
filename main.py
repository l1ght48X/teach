import json
import os
from datetime import datetime
from collections import Counter

DATA_FILE = "books.json"

def load_books():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books(books):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

# --- Функции бизнес-логики ---

def add_book(books):
    print("\n--- Добавление новой книги ---")
    
    author = input("Введите автора: ").strip()
    title = input("Введите название: ").strip()

    if any(b for b in books if b['автор'].lower() == author.lower() and b['название'].lower() == title.lower()):
        print("⚠ Эта книга уже есть в вашем списке.")
        return

    while True:
        rating = input("Введите вашу оценку (от 1 до 5): ")
        if rating.isdigit() and 1 <= int(rating) <= 5:
            rating = int(rating)
            break
        else:
            print("❌ Оценка должна быть целым числом от 1 до 5.")

    while True:
        date_str = input("Введите дату прочтения (ГГГГ-ММ-ДД): ").strip()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌ Неверный формат даты. Используйте ГГГГ-ММ-ДД (например, 2024-05-20).")

    new_book = {
        "автор": author,
        "название": title,
        "оценка": rating,
        "дата_прочтения": date.isoformat()
    }
    books.append(new_book)
    save_books(books)
    print("✅ Книга успешно добавлена!")

def show_all_books(books):
    print("\n--- Ваш список книг ---")
    if not books:
        print("Список пуст.")
        return

    for i, book in enumerate(books, 1):
        print(f"{i}. {book['автор']} — «{book['название']}»")
        print(f"   Оценка: {book['оценка']} | Дата: {book['дата_прочтения']}")

def show_average_rating(books):
    print("\n--- Средняя оценка ---")
    if not books:
        print("Список пуст.")
        return

    total = sum(book['оценка'] for book in books)
    average = total / len(books)
    print(f"Средняя оценка ваших книг: {average:.2f}")

def show_author_stats(books):
    print("\n--- Статистика по авторам ---")
    if not books:
        print("Список пуст.")
        return

    authors = [book['автор'] for book in books]
    stats = Counter(authors)
    
    for author, count in stats.items():
        print(f"{author}: {count} {'книга' if count == 1 else 'книги'}")

def delete_book(books):
    print("\n--- Удаление книги ---")
    show_all_books(books)
    
    if not books:
        return

    try:
        index = int(input("Введите номер книги для удаления: ")) - 1
        if 0 <= index < len(books):
            removed_book = books.pop(index)
            save_books(books)
            print(f"✅ Книга «{removed_book['название']}» удалена.")
        else:
            print("❌ Неверный номер книги.")
    except ValueError:
        print("❌ Введите корректный номер.")

def main():
    books = load_books()
    
    menu_actions = {
        "1": add_book,
        "2": show_all_books,
        "3": show_average_rating,
        "4": show_author_stats,
        "5": delete_book,
    }

    while True:
        print("\n=== Трекер прочитанных книг ===")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == "6":
            print("До свидания!")
            break
        
        action = menu_actions.get(choice)
        
        if action:
            action(books) # Передаем список книг в функцию
            # Небольшая пауза, чтобы пользователь успел прочитать результат
            input("\nНажмите Enter, чтобы продолжить...")
            os.system('cls' if os.name == 'nt' else 'clear') # Очистка консоли (Windows/Mac/Linux)
        else:
            print("❌ Неверный выбор. Пожалуйста, введите число от 1 до 6.")

if __name__ == "__main__":
    main()
