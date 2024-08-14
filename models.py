from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        # Перевірка, чи номер має 10 цифр
        if len(self.value) != 10 or not self.value.isdigit():
            raise ValueError(
                "Invalid phone number format. Please provide a 10-digit numeric phone number.")


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_email()

    def validate_email(self):
        if "@" not in self.value or "." not in self.value:
            raise ValueError(
                "Invalid email format. Please provide a valid email address.")


class Address(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [
            phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break

    def find_phone(self, target_number):
        result = list(filter(lambda phone: phone.value ==
                      target_number, self.phones))
        return result[0] if len(result) > 0 else None

    def add_birthday(self, birthday):
        if self.birthday is None:
            self.birthday = birthday
        else:
            raise ValueError("Birthday already exists")

    def show_birthday(self):
        return self.birthday

    def add_email(self, email):
        if self.email is None:
            self.email = Email(email)
        else:
            raise ValueError("Email already exists.")

    def add_address(self, address):
        if self.address is None:
            self.address = Address(address)
        else:
            raise ValueError("Address already exists.")

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        email_str = self.email.value if self.email else "No email"
        address_str = self.address.value if self.address else "No address"
        birthday_str = self.birthday.value.strftime(
            '%d.%m.%Y') if self.birthday else "No birthday"
        return f"Name: {self.name.value}, Phone: {phones_str}, Email: {email_str}, Address: {address_str}, Birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self) -> list[dict]:
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    continue
                diff_in_days = (birthday_this_year - today).days
                # 0 - Sunday
                if diff_in_days <= 7 and ['0', '6'].count(birthday_this_year.strftime('%w')) == 0:
                    upcoming_birthdays.append(
                        {'name': record.name.value, 'congratulation_date': birthday_this_year.strftime("%d.%m.%Y")})
        return upcoming_birthdays

    def __str__(self):
        contacts = []
        for record in self.data.values():
            phones_str = '; '.join(p.value for p in record.phones)
            email_str = record.email.value if hasattr(
                record, 'email') and record.email else "No email"
            address_str = record.address.value if hasattr(
                record, 'address') and record.address else "No address"

            if isinstance(record.birthday, Birthday):
                birthday_str = record.birthday.value.strftime('%d.%m.%Y')
            elif isinstance(record.birthday, str):
                birthday_str = record.birthday  # Якщо це рядок, вважаємо його правильним форматом
            else:
                birthday_str = "No birthday"

            contacts.append(
                f"Name: {record.name.value}, Phone: {phones_str}, Email: {email_str}, Address: {address_str}, Birthday: {birthday_str}")
        return "\n".join(contacts)
