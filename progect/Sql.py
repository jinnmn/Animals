from datetime import date

import mysql.connector
import json
import Animal

class MySQLDatabase:
    def __init__(self, db_name, user, password, host="localhost"):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.connection = None
        self.cursor = None
        self._connect()

    def _connect(self):
        """Устанавливаем подключение к базе данных MySQL."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            # Проверяем, существует ли база данных, если нет - создаем её
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            self.connection.database = self.db_name
        except mysql.connector.Error as err:
            print(f"Ошибка подключения: {err}")

    def create_table(self):
        """Создаем таблицу для животных в базе данных."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS animals (
            id INT PRIMARY KEY,
            type ENUM('Dog', 'Cat', 'Hamster', 'Horse', 'Donkey') NOT NULL,
            name VARCHAR(255),
            birth_date DATE,
            commands JSON
        )
        """
        self.cursor.execute(create_table_query)

    def insert_animal(self, animal: Animal):
        """Добавляем животное в таблицу."""
        animal_type = animal.__class__.__name__  # Получаем название класса (типа животного)
        insert_query = """
        INSERT INTO animals (id, type, name, birth_date, commands)
        VALUES (%s, %s, %s, %s, %s)
        """
        commands_json = json.dumps(animal.commands_())  # Преобразуем список команд в JSON
        self.cursor.execute(insert_query, (animal_type, animal.get_name(), animal.get_birth_date(), commands_json))
        self.connection.commit()

    def fetch_all_animals(self):
        """Получаем все данные о животных из базы данных."""
        self.cursor.execute("SELECT * FROM animals")
        return self.cursor.fetchall()

    def close(self):
        """Закрываем соединение с базой данных."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


# Пример использования класса
if __name__ == '__main__':
    db = MySQLDatabase(db_name="animal_shelter", user="root", password="260989")

    # Создаем таблицу, если её еще нет
    db.create_table()

    # Создаем объекты животных
    dog = Animal.Dog('Bobik', date(2017, 1, 1))
    cat = Animal.Cat('Murka', date(2019, 5, 15))

    # Вставляем данные в базу данных
    db.insert_animal(1, "Собака", dog.__str__(), dog.get_birth_date(), dog.commands_())
    db.insert_animal(2, "Кошка", cat.__str__(), cat.get_birth_date(), cat.commands_())

    # Получаем и выводим все данные о животных из базы данных
    animals = db.fetch_all_animals()
    for animal in animals:
        print(animal)

    # Закрываем подключение с базой данных
    db.close()