import sys
from datetime import date
import Animal
import Sql
from Counter import Counter


class Menu:

    def __init__(self, db: Sql.MySQLDatabase):
        self.db = db
        self.counter = Counter()

    def show_menu(self):
        print("\nМеню:")
        print("1. Добавить животное в базу данных")
        print("2. Показать все животные в базе данных")
        print("3. Показать информацию о животном по ID")
        print("4. Взаимодействовать с животным")
        print("5. Добавить команду")
        print("6. Выход")
        choice = input("Выберите действие (1-6): ")
        return choice

    def add_animal(self):
        print("\nДобавление животного:")
        name = input("Введите имя животного: ")
        try:
            birth_date = input("Введите дату рождения животного (гггг-мм-дд): ")
            birth_date = date.fromisoformat(birth_date)
        except Exception as e:
            print('Неверно введена дата')
            self.add_animal()
        print("\nВыберите тип животного:")
        print("1. Собака")
        print("2. Кошка")
        print("3. Хомяк")
        print("4. Лошадь")
        print("5. Осел")
        animal_choice = input("Выберите тип животного (1-5): ")

        if animal_choice == "1":
            animal = Animal.Dog(name, birth_date)
        elif animal_choice == "2":
            animal = Animal.Cat(name, birth_date)
        elif animal_choice == "3":
            animal = Animal.Hamster(name, birth_date)
        elif animal_choice == "4":
            animal = Animal.Horse(name, birth_date)
        elif animal_choice == "5":
            animal = Animal.Donkey(name, birth_date)
        else:
            print("Неверный выбор! Попробуйте снова.")
            return
        try:
            self.db.insert_animal(animal)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        else:
            self.counter.add()
            print(f'{animal} создано. Счетчик новых животных:{self.counter.get_count()}')

    def show_all_animals(self):
        print("\nВсе животные в базе данных:")
        self.db.fetch_all_animals_info()

    def show_animal_by_id(self):
        try:
            animal_id = int(input("\nВведите ID животного: "))
            animal = self.db.fetch_animal_by_id(animal_id)
            if animal:
                print(animal)
        except ValueError:
            print("Неверный ввод! Введите корректный ID.")

    def interact_with_animal(self):
        print("\nВыберите животное для взаимодействия:")
        self.db.fetch_all_animals_info()
        try:
            animal_id = int(input("\nВведите ID животного для взаимодействия: "))
            animal = self.db.fetch_animal_by_id(animal_id)
            if animal:
                animal.show_skills()
                command = input("Выберите команду для животного: ")
                if command in animal.commands_():
                    animal.do_act(command)
                else:
                    print("Команда не найдена.")
        except ValueError:
            print("Неверный ввод! Введите корректный ID.")

    def add_command(self):
        print("\nВыберите животное для взаимодействия:")
        self.db.fetch_all_animals_info()
        try:
            animal_id = int(input("\nВведите ID животного для взаимодействия: "))
            animal = self.db.fetch_animal_by_id(animal_id)
            if animal:
                command = input("ВВедите название команды:")
                action = input('Введите результат команды:')
                animal.add_command(
                    command, action)
                self.db.update_commands(animal, animal_id)
        except ValueError:
            print("Неверный ввод! Введите корректный ID.")

    def start(self):
        while True:
            choice = self.show_menu()
            if choice == "1":
                self.add_animal()
            elif choice == "2":
                self.show_all_animals()
            elif choice == "3":
                self.show_animal_by_id()
            elif choice == "4":
                self.interact_with_animal()
            elif choice == "5":
                self.add_command()
            elif choice == "6":
                print("Выход из программы.")
                db.close()                      # Закрываем БД
                sys.exit()
            else:
                print("Неверный выбор! Попробуйте снова.")


if __name__ == '__main__':
    db = Sql.MySQLDatabase(db_name="animal_shelter", user="root", password="260989")
    db.create_table()
    menu = Menu(db)
    menu.start()
