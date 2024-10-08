from collections import UserDict
from datetime import datetime
import re
from special_efects import *


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
            combed_msg = error_msg4return(
                "Invalid phone number format. Please provide a 10-digit numeric phone number."
            )
            raise ValueError(combed_msg)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            combed_msg = error_msg4return("Invalid date format. Use DD.MM.YYYY")
            raise ValueError(combed_msg)


class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_email()

    def validate_email(self):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, self.value):
            combed_msg = error_msg4return(
                "Invalid email format. Please provide a valid email address."
            )
            raise ValueError(combed_msg)


class Address(Field):
    def __init__(self, value):
        super().__init__(value)


class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags or []

    def __str__(self):
        tags_str = ", ".join(self.tags)
        return f"Title: {self.title}, Content: {self.content}, Tags: {tags_str}"

    def add_tags(self, tags):
        self.tags.extend(tags)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.last_name = None
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None
        self.notes = []

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
        if isinstance(birthday, str):
            birthday = Birthday(birthday)
        if self.birthday is None:
            self.birthday = birthday
        else:
            combed_msg = error_msg4return("Birthday already exists")
            raise ValueError(combed_msg)

    def show_birthday(self):
        return self.birthday

    def add_email(self, email):
        if self.email is None:
            self.email = Email(email)
        else:
            combed_msg = error_msg4return("Email already exists")
            raise ValueError(combed_msg)

    def add_address(self, address):
        if self.address is None:
            self.address = Address(address)
        else:
            combed_msg = error_msg4return("Address already exists")
            raise ValueError(combed_msg)

    def add_note(self, title, content):
        self.notes.append(Note(title, content))

    def show_notes(self):
        if not self.notes:
            return info_msg4return("No notes available.")
        return "\n".join(
            f"Title: {note.title}, Content: {note.content}, Tags: {', '.join(note.tags)}"
            for note in self.notes
        )

    def find_notes_by_tag(self, tag):
        matching_notes = [note for note in self.notes if tag in note.tags]
        if not matching_notes:
            return info_msg4return(f"No notes found with the tag: {tag}")
        return matching_notes

    def sort_notes_by_tags(self):
        sorted_notes = sorted(self.notes, key=lambda note: ",".join(sorted(note.tags)))
        return sorted_notes

    def __str__(self):
        last_name_str = " " + self.last_name if self.last_name else ""
        phones_str = "; ".join(p.value for p in self.phones)
        email_str = self.email.value if self.email else ""
        address_str = self.address.value if self.address else ""

        if isinstance(self.birthday, Birthday):
            birthday_str = self.birthday.value.strftime("%d.%m.%Y")
        elif isinstance(self.birthday, str):
            birthday_str = self.birthday
        else:
            birthday_str = "No birthday"
        notes_str = self.show_notes()
        return (
            f"Name: {self.name.value + last_name_str}, Phone: {phones_str}, "
            + f"Email: {email_str}, Address: {address_str}, "
            + f"Birthday: {birthday_str}, Notes: {notes_str}"
        )


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
                if (
                    diff_in_days <= 7
                    and ["0", "6"].count(birthday_this_year.strftime("%w")) == 0
                ):
                    upcoming_birthdays.append(
                        {
                            "name": record.name.value,
                            "congratulation_date": birthday_this_year.strftime(
                                "%d.%m.%Y"
                            ),
                        }
                    )
        return upcoming_birthdays

    def search(self, keyword):
        results = AddressBook()
        for record in self.data.values():
            if (
                keyword.lower() in record.name.value.lower()
                or any(
                    keyword.lower() in phone.value.lower() for phone in record.phones
                )
                or (
                    record.birthday
                    and keyword.lower()
                    in record.birthday.value.strftime("%d.%m.%Y").lower()
                )
                or (record.email and keyword.lower() in record.email.value.lower())
                or (record.address and keyword.lower() in record.address.value.lower())
                or any(
                    keyword.lower() in note.title.lower()
                    or keyword.lower() in note.content.lower()
                    or keyword.lower() in tag.lower()
                    for note in record.notes
                    for tag in note.tags
                )
            ):
                results.add_record(record)
        return results

    def __str__(self):
        contacts = []
        for record in self.data.values():
            if not hasattr(record, "last_name"):
                record.last_name = None
            last_name_str = record.last_name if record.last_name else "No last name"
            phones_str = (
                "; ".join(p.value for p in record.phones)
                if record.phones
                else "No phone"
            )
            email_str = (
                record.email.value
                if hasattr(record, "email") and record.email
                else "No email"
            )
            address_str = (
                record.address.value
                if hasattr(record, "address") and record.address
                else "No address"
            )

            if isinstance(record.birthday, Birthday):
                birthday_str = record.birthday.value.strftime("%d.%m.%Y")
            elif isinstance(record.birthday, str):
                birthday_str = record.birthday
            else:
                birthday_str = "No birthday"

            notes_str = "\n  ".join(
                f"{i+1}. {note.title}: {note.content}"
                for i, note in enumerate(record.notes)
            )
            if not notes_str:
                notes_str = "No notes"

            contacts.append(
                f"First Name: {record.name.value}\n"
                + f"Last Name: {last_name_str}\n"
                + f"Phone: {phones_str}\n"
                + f"Email: {email_str}\n"
                + f"Address: {address_str}\n"
                + f"Birthday: {birthday_str}\n"
                + f"Notes:\n {notes_str}"
            )
        return "\n\n".join(contacts)
