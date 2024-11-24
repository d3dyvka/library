import json

def load_file(file_name):
    with open(f'{file_name}.json', 'r') as library_file:
        library_data = json.load(library_file)
        return library_data
def delete(library_data, file_name):
    display(library_data=library_data)
    max_id = max(book['id'] for book in library_data) if library_data else 1
    id = int(input("Введите id книги для удаления:"))

    book_to_delete = next((book for book in library_data if book['id'] == id), None)

    if (id <= max_id) and (id >= 1):
        library_data.remove(book_to_delete)
        with open(f'{file_name}.json', 'w', encoding='utf-8') as f:
            json.dump(library_data, f, ensure_ascii=False, indent=4)
    else:
        print("Некоректно веденно значение id")
def add(library_data, file_name):
    title = input("Введите название книги:")
    author = input("Введите имя автора:")
    year = int(input("Введите год выпуска книги:"))
    new_id = max(book['id'] for book in library_data) + 1 if library_data else 1
    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "year": year,
        "status": "в наличии"
    }
    library_data.append(new_book)
    with open(f'{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(library_data, f, ensure_ascii=False, indent=4)


def search(library_data):
    print("Поиск книги. Выберите критерий:")
    print("1. По году выпуска")
    print("2. По названию")
    print("3. По автору")

    # Ввод критерия поиска
    choice = input(": ").strip()

    if choice == "1":
        year = int(input("Введите год выпуска книги: "))
        results = [book for book in library_data if book['year'] == year]
    elif choice == "2":
        title = input("Введите название книги: ").strip().lower()
        results = [book for book in library_data if title in book['title'].lower()]
    elif choice == "3":
        author = input("Введите автора книги: ").strip().lower()
        results = [book for book in library_data if author in book['author'].lower()]
    else:
        print("Некорректный выбор. Попробуйте снова.")
        return

    # Вывод результатов
    if results:
        for book in results:
            print(json.dumps(book, ensure_ascii=False, indent=4))
    else:
        print("Книги по заданному критерию не найдены.")


def display(library_data):
    print(json.dumps(library_data, indent=4).encode('utf-8').decode('unicode_escape'))


def update_status(library_data, file_name):
    # Ввод ID книги
    book_id = int(input("Введите ID книги для обновления статуса: "))

    # Поиск книги с указанным ID
    book_to_update = next((book for book in library_data if book['id'] == book_id), None)

    if book_to_update:
        # Ввод нового статуса
        new_status = input("Введите новый статус книги (в наличии/выдана): ").strip().lower()

        # Проверка введенного статуса
        if new_status not in ["в наличии", "выдана"]:
            print("Неверный статус. Статус должен быть либо 'в наличии', либо 'выдана'.")
            return

        # Обновляем статус
        book_to_update['status'] = new_status
        print(f"Статус книги с id {book_id} успешно обновлен на '{new_status}'.")

        # Сохраняем изменения в файл
        with open(f'{file_name}.json', 'w', encoding='utf-8') as file:
            json.dump(library_data, file, ensure_ascii=False, indent=4)
    else:
        print(f"Книга с id {book_id} не найдена.")
