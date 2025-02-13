from abc import ABC
from datetime import date


class Animal(ABC):
    def __init__(self, name: str, b_date: date):
        self.__name = name
        self._commands = {'Спать': "спит."}
        self.__b_date = b_date

    def __str__(self):
        return f'Животное типа {self.__class__.__name__} по кличке {self.__name}'

    def do_act(self, action):
        print(f'{self.__name} {self._commands[action]}')

    def show_skills(self):
        print(f'{self} может:')
        print(' ', *list(self._commands.keys()))

    def commands_(self):
        return dict(self._commands)  # дабы словарь инкапсулировать

    def add_command(self, key, value):
        if key not in self._commands:
            self._commands[key] = value
        else:
            print('Уже умеет!')


class HomeAnimal(Animal):
    def __init__(self, name: str, b_date: date):
        super().__init__(name, b_date)
        self._commands['Есть'] = 'ест из миски.'
        self._commands['Играть'] = 'весело резвится.'


class WorkAnimal(Animal):
    def __init__(self, name: str, b_date: date):
        super().__init__(name, b_date)
        self._commands['Есть'] = 'ест из кормушки.'
        self._commands['Тянуть'] = 'везет повозку.'


class Dog(HomeAnimal):
    def __init__(self, name: str, b_date: date):
        super().__init__(name, b_date)
        self._commands['Лаять'] = 'весело гавкает!'


class Cat(HomeAnimal):
    def __init__(self, name: str, b_date: date):
        super().__init__(name, b_date)
        self._commands['Мяукать'] = 'мило мяукает!'


class Hamster(HomeAnimal):
    def __init__(self, name: str, b_date: date):
        super().__init__(name, b_date)
        self._commands['Пищать'] = 'тихо попискивает!'


class Horse(WorkAnimal):
    def __init__(self, name: str, b_date: date):
        super().__init__(name, b_date)
        self._commands['Ржать'] = 'весело ржет!'


class Donkey(WorkAnimal):
    def __init__(self, name: str, b_date: date):
        super().__init__(name, b_date)
        self._commands['Реветь'] = 'громко ревет!'


if __name__ == '__main__':
    dog = Horse('Bobik', date(2017, 1, 1))
    print(dog)
    dog.show_skills()
    dog.add_command('Купаться', 'купается')
    dog.add_command('Спать', 'купается')
    for x in dog.commands_():
        dog.do_act(x)
