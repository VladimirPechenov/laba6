# main.py
import mysql.connector
from db import (
    list_categories, add_category, update_category, delete_category,
    list_brands,
    list_products, add_product, update_product, delete_product,
    get_products_in_category, get_low_stock_products
)
from datetime import datetime


def print_menu():
    print("\n=== МЕНЮ ===")
    print("1. Показать категории")
    print("2. Добавить категорию")
    print("3. Редактировать категорию")
    print("4. Удалить категорию")
    print("5. Показать бренды")
    print("6. Показать товары")
    print("7. Добавить товар")
    print("8. Редактировать товар")
    print("9. Удалить товар")
    print("10. Анализ: товары в категории")
    print("11. Анализ: низкий остаток")
    print("0. Выход")


def get_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Введите число не меньше {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Введите число не больше {max_val}.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите целое число.")


def get_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Ошибка: введите дату в формате YYYY-MM-DD.")


def get_bool(prompt):
    while True:
        val = input(prompt + " (1/0): ")
        if val == '1': return True
        if val == '0': return False
        print("Ошибка: введите 1 или 0.")


def main():
    while True:
        print_menu()
        choice = input("Выберите пункт: ")
        try:
            if choice == '1':
                for cid, name, desc in list_categories(): print(cid, name, desc)

            elif choice == '2':
                n = input("Название: ").strip()
                d = input("Описание: ").strip()
                if not n:
                    print("Ошибка: название не может быть пустым.")
                else:
                    add_category(n, d)
                    print("Категория добавлена.")

            elif choice == '3':
                cid = get_int("ID категории: ", min_val=1)
                n = input("Новое название: ").strip()
                d = input("Новое описание: ").strip()
                if not n:
                    print("Ошибка: название не может быть пустым.")
                else:
                    update_category(cid, n, d)
                    print("Категория обновлена.")

            elif choice == '4':
                cid = get_int("ID категории: ", min_val=1)
                delete_category(cid)
                print("Категория удалена.")

            elif choice == '5':
                for bid, name, country in list_brands(): print(bid, name, country)

            elif choice == '6':
                for p in list_products(): print(p)

            elif choice == '7':
                name = input("Название товара: ").strip()
                if not name:
                    print("Ошибка: название не может быть пустым.")
                    continue
                desc = input("Описание: ").strip()
                avail = get_bool("В наличии")
                date_add = get_date("Дата добавления (YYYY-MM-DD): ")
                stock = get_int("Остаток: ", min_val=0)

                print("Категории:")
                for cid, nm, _ in list_categories(): print(cid, nm)
                cat_id = get_int("ID категории: ", min_val=1)

                print("Бренды:")
                for bid, nm, _ in list_brands(): print(bid, nm)
                brand_id = get_int("ID бренда: ", min_val=1)

                add_product(name, desc, avail, date_add, stock, brand_id, cat_id)
                print("Товар добавлен.")

            elif choice == '8':
                pid = get_int("ID товара: ", min_val=1)
                name = input("Новое название: ").strip()
                if not name:
                    print("Ошибка: название не может быть пустым.")
                    continue
                desc = input("Новое описание: ").strip()
                avail = get_bool("В наличии")
                date_add = get_date("Дата (YYYY-MM-DD): ")
                stock = get_int("Остаток: ", min_val=0)

                print("Категории:")
                for cid, nm, _ in list_categories(): print(cid, nm)
                cat_id = get_int("ID категории: ", min_val=1)

                print("Бренды:")
                for bid, nm, _ in list_brands(): print(bid, nm)
                brand_id = get_int("ID бренда: ", min_val=1)

                update_product(pid, name, desc, avail, date_add, stock, brand_id, cat_id)
                print("Товар обновлен.")

            elif choice == '9':
                pid = get_int("ID товара: ", min_val=1)
                delete_product(pid)
                print("Товар удалён.")

            elif choice == '10':
                cid = get_int("ID категории: ", min_val=1)
                for row in get_products_in_category(cid): print(row)

            elif choice == '11':
                thr = get_int("Порог остатка: ", min_val=0)
                for row in get_low_stock_products(thr): print(row)

            elif choice == '0':
                print("Выход...")
                break

            else:
                print("Неверный выбор.")

        except mysql.connector.Error as db_err:
            print(f"Ошибка работы с БД: {db_err}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    main()