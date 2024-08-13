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
            raise ValueError("Invalid phone number format. Please provide a 10-digit numeric phone number.")

class Birthday(Field):
    def __init__(self, value):
        try:            
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break

    def find_phone(self, target_number):
        result = list(filter(lambda phone: phone.value == target_number, self.phones))
        return result[0] if len(result) > 0 else None

    def add_birthday(self, birthday):
        if self.birthday is None:
            self.birthday = birthday
        else:
            raise ValueError("Birthday already exists")
        
    def show_birthday(self):
        return self.birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

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
                if diff_in_days <= 7 and ['0', '6'].count(birthday_this_year.strftime('%w')) == 0:  # 0 - Sunday
                    upcoming_birthdays.append({'name': record.name.value, 'congratulation_date': birthday_this_year.strftime("%d.%m.%Y")})
        return upcoming_birthdays

    def __str__(self):
        contacts = []
        for record in self.data.values():
            birthday_str = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else "No birthday"
            contacts.append(f"Name: {record.name.value}, Phone: {'; '.join(p.value for p in record.phones)}, Birthday: {birthday_str}")
        return "\n".join(contacts)
