class Counter:
    def __init__(self):
        self._count = 0
        self._used_in_try = False
        self._is_open = True

    def add(self):
        self._count += 1

    def get_count(self):
        return self._count

    def __enter__(self):
        self._used_in_try = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._is_open = False
        if exc_type is not None:
            print(f"Произошла ошибка: {exc_value}")
        return True  # Исключения будут подавлены

    def reset(self):
        self._count = 0
        self._is_open = True
        self._used_in_try = False
