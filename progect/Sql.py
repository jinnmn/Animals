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
            id INT AUTO_INCREMENT PRIMARY KEY,
            type ENUM('Dog', 'Cat', 'Horse', 'Hamster', 'Donkey') NOT NULL,
            name VARCHAR(255),
            birth_date DATE,
            commands JSON
        )
        """
        self.cursor.execute(create_table_query)

    def check_animal_exists(self, animal):
        """Проверяем, существует ли животное с таким же именем и датой рождения."""
        query = """
        SELECT COUNT(*) FROM animals WHERE name = %s AND birth_date = %s
        """
        self.cursor.execute(query, (animal.get_name(), animal.get_birth_date()))
        result = self.cursor.fetchone()
        return result[0] > 0  # Если результат больше 0, значит животное уже существует

    def insert_animal(self, animal):
        """Добавляем животное в таблицу."""
        if self.check_animal_exists(animal):
            print(f"Животное с именем {animal.get_name()} и датой рождения {animal.get_birth_date()} уже существует.")
            return

        animal_type = animal.__class__.__name__  # Получаем название класса (типа животного)
        insert_query = """
        INSERT INTO animals (type, name, birth_date, commands)
        VALUES (%s, %s, %s, %s)
        """
        commands_json = json.dumps(animal.commands_())  # Преобразуем список команд в JSON
        self.cursor.execute(insert_query, (animal_type, animal.get_name(), animal.get_birth_date(), commands_json))
        self.connection.commit()

    def fetch_animal_by_id(self, animal_id):
        """Получаем данные о животном по ID и создаем соответствующий объект."""
        query = "SELECT * FROM animals WHERE id = %s"
        self.cursor.execute(query, (animal_id,))
        row = self.cursor.fetchone()

        if row:
            # Если животное найдено, создаем объект животного
            return self.create_animal_from_row(row)
        else:
            # Если животное с таким ID не найдено
            print(f"Животное с ID {animal_id} не найдено.")
            return None

    def create_animal_from_row(self, row):
        """Создаем объект животного из строки результата SQL-запроса."""
        animal_type = row[1]  # Тип животного
        name = row[2]  # Имя животного
        birth_date = row[3]  # Дата рождения животного
        commands = json.loads(row[4])  # Преобразуем строку JSON в словарь команд

        # Создаем объект животного в зависимости от его типа
        if animal_type == 'Dog':
            animal = Animal.Dog(name, birth_date)
        elif animal_type == 'Cat':
            animal = Animal.Cat(name, birth_date)
        elif animal_type == 'Hamster':
            animal = Animal.Hamster(name, birth_date)
        elif animal_type == 'Horse':
            animal = Animal.Horse(name, birth_date)
        elif animal_type == 'Donkey':
            animal = Animal.Donkey(name, birth_date)
        else:
            raise ValueError(f"Неизвестный тип животного: {animal_type}")

        # Добавляем команды животного
        for command, description in commands.items():
            animal.add_command(command, description)

        return animal

    def fetch_all_animals_info(self):
        """Получаем все данные о животных из базы данных (ID, тип, имя и дата рождения)."""
        query = "SELECT id, type, name, birth_date FROM animals"
        self.cursor.execute(query)
        animals = self.cursor.fetchall()

        # Выводим информацию о каждом животном
        print(f"{'ID':<5} {'Тип':<10} {'Имя':<20} {'Дата рождения':<15}")
        print('-' * 50)
        for animal in animals:
            birth_date = animal[3].strftime('%Y-%m-%d') if animal[3] else 'Неизвестно'
            print(f"{animal[0]:<5} {animal[1]:<10} {animal[2]:<20} {birth_date:<15}")

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

    db.fetch_all_animals_info()
    # Создаем объекты животных
    dog = Animal.Dog('Bobik', date(2017, 1, 1))
    cat = Animal.Cat('Murka', date(2019, 5, 15))

    # Вставляем данные в базу данных
    db.insert_animal(dog)
    db.insert_animal(cat)


    # Закрываем подключение с базой данных
    db.close()
