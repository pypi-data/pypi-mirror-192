class Student:
    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname

    def say_hello(self) -> str:
        return "¡Hello, {} {}! ¡Welcome to class!".format(self.name, self.surname)
