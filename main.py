from collections import UserDict

from decorators import error_handler


class NoContactError(Exception):
    pass


class NameInputError(Exception):
    pass


class PhoneInputError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise NameInputError("Incorrect name")

        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        if (
            not value
            or not isinstance(value, str)
            or len(value) != 10
            or not value.isascii()
            or not value.isdigit()
        ):
            raise PhoneInputError("Phone number must contain exactly 10 digits")

        super().__init__(value)


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    @error_handler
    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        self.phones = [
            filtered_phone
            for filtered_phone in self.phones
            if filtered_phone.value != phone
        ]

    @error_handler
    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        self.phones = [
            Phone(new_phone) if phone.value == old_phone else phone
            for phone in self.phones
        ]

    def find_phone(self, phone: str) -> Phone | None:
        return next((item for item in self.phones if item.value == phone), None)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    @error_handler
    def find(self, name: str) -> Record | None:
        if name not in self.data:
            raise NoContactError(f"Contact with name {name} does not exist")
        return self.data[name]

    @error_handler
    def delete(self, name: str) -> None:
        if name not in self.data:
            raise NoContactError(f"Contact with name {name} does not exist")
        self.data.pop(name)


def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()
