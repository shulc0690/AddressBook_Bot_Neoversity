from addressbook_bot.models import AddressBook, Birthday, Record, Email, Address
import re
from datetime import datetime, timedelta


def input_error(func):
    """Validator on exceptions."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as err:
            return err
        except TypeError as err:
            return err
    return inner

def validate_phone(phone):
    """Validates that the phone number contains exactly 10 digits."""
    if re.fullmatch(r'\d{10}', phone):
        return True
    else:
        raise ValueError("Phone number must contain exactly 10 digits.")

def validate_name(name):
    """Validates that the name or last name contains only letters and is a single word."""
    if re.fullmatch(r'[A-Za-zА-Яа-яЇїІіЄєҐґ]+', name):
        return True
    else:
        raise ValueError("Name and Last Name must contain only letters and be a single word.")

@input_error
def parse_input(user_input):
    """Function parses input."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    if not args or not args[0].strip() or len(args) > 1:
        return "Error: Name must be a single word without spaces. Please provide a valid name."
    
    name = args[0].strip()
    
    try:
        validate_name(name)
    except ValueError as e:
        return f"Error: {e}"

    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name=name)
        book.add_record(record)
        message = "Contact added."

    last_name = input("Enter last name (or press Enter to skip): ").strip()
    for attempt in range(2):
        if last_name:
            try:
                validate_name(last_name)
                record.last_name = last_name
                break
            except ValueError as e:
                if attempt < 1:
                    print(f"Error: {e}. You have {1 - attempt} attempt left.")
                    last_name = input("Re-enter last name: ").strip()
                else:
                    print(f"Error: {e}. Last Name not added.")

    for i in range(2):
        phone = input(
            "Enter phone number (10 digits) (or press Enter to skip): ").strip()
        if not phone:
            break
        try:
            record.add_phone(phone)
            break
        except ValueError as e:
            print(e)

    for i in range(2):
        email = input("Enter email address (or press Enter to skip): ").strip()
        if not email:
            break
        try:
            record.add_email(email)
            break
        except ValueError as e:
            print(e)


    for i in range(2):
        address = input("Enter address (or press Enter to skip): ").strip()
        if not address:
            break
        record.add_address(address)
        break

    for i in range(2):
        birthday = input(
            "Enter birthday (DD.MM.YYYY) (or press Enter to skip): ").strip()
        if not birthday:
            break
        try:
            record.add_birthday(birthday)
            break
        except ValueError as e:
            print(e)

    return message


@input_error
def edit_contact(args, book: AddressBook):
    """Function changes existing contact."""
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = "Phone updated."

    if record is None:
        message = "Contact does not exists."
    if new_phone and old_phone:
        record.edit_phone(old_phone, new_phone)
    return message


@input_error
def get_contact(args, book: AddressBook):
    """Function get phone for existing contact."""
    if len(args) < 1:
        return "Error: Please provide a contact name."
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact does not exists."
    return record

@input_error
def search_contact(args, book: AddressBook):
    """Function search contact by all fields."""
    if len(args) < 1:
        return "Error: Please provide a keyword."
    keyword, *_ = args
    records = book.search(keyword)
    if records is None:
        return "There is no contact that matches the search data."
    return records

def show_address_book(book: AddressBook):
    """Function returns all contacts."""
    if len(book) == 0:
        return "Contact list is empty."
    return book


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Error: Please provide a contact name and a birthday."
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        # Якщо контакт не існує, створюємо новий запис
        record = Record(name=name)
        book.add_record(record)
        message = f"Contact '{name}' created."
    else:
        message = "Contact found."
    
    try:
        # Створюємо об'єкт Birthday, передаючи в нього строку дати
        birthday = Birthday(birthday_str)
        record.add_birthday(birthday.value.strftime('%d.%m.%Y'))
        return f"{message} Birthday added."
    except ValueError as e:
        return f"Error: {e}"

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact does not exists."
    return record.birthday.value.strftime('%d.%m.%Y')

@input_error
def edit_birthday(args, book):
    if len(args) < 2:
        return "Error: Please provide a contact name and a new birthday."
    name, new_birthday_str, *_ = args
    record = book.find(name)
    
    if record is None:
        return "Contact does not exist."
    
    try:
        new_birthday = Birthday(new_birthday_str)
        record.birthday = new_birthday
        return f"Birthday for {name} has been updated to {new_birthday_str}."
    except ValueError as e:
        return f"Error: {e}"

@input_error
def delete_birthday(args, book):
    if len(args) < 1:
        return "Error: Please provide a contact name."
    name, *_ = args
    record = book.find(name)
    
    if record is None:
        return "Contact does not exist."
    
    if record.birthday is None:
        return f"{name} does not have a birthday set."
    
    record.birthday = None
    return f"Birthday for {name} has been deleted."


@input_error
def birthdays(book: AddressBook, days: int):
    today = datetime.today().date()
    target_date = today + timedelta(days=days)
    upcoming_birthdays = []

    for record in book.data.values():
        if record.birthday:
            birthday = record.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday
            
            if today <= birthday_this_year <= target_date:
                upcoming_birthdays.append(
                    {'name': record.name.value, 'birthday': birthday.strftime("%d.%m.%Y")}
                )

    if not upcoming_birthdays:
        return f"No birthdays within the next {days} days."
    
    result = f"Birthdays within the next {days} days:\n"
    for entry in upcoming_birthdays:
        result += f"- {entry['name']} on {entry['birthday']}\n"
    return result.strip()

@input_error
def add_note_to_contact(args, book: AddressBook):
    if len(args) < 1:
        return "Error: Please provide a contact name."
    
    name = args[0]
    record = book.find(name)
    
    if record is None:
        return "Contact does not exist."

    title = input("Enter note title: ").strip()
    content = input("Enter note content: ").strip()
    tags = input("Enter tags (separated by commas):").strip().split(",")
    record.add_note(title, content)
    record.notes[-1].add_tags([tag.strip() for tag in tags if tag.strip()])
    return "Note added successfully."

def find_notes_by_tag(args, book: AddressBook):
    if len(args) < 2:
        return "Error: Please provide a contact name and a tag."
    
    name = args[0]
    tag = args[1]
    record = book.find(name)
    
    if record is None:
        return "Contact does not exist."
    
    matching_notes = record.find_notes_by_tag(tag)
    
    if isinstance(matching_notes, str): 
        return matching_notes
    
    return "\n".join(str(note) for note in matching_notes)

@input_error
def sort_notes_by_tags(args, book: AddressBook):
    if len(args) < 1:
        return "Error: Please provide a contact name."
    
    name = args[0]
    record = book.find(name)
    
    if record is None:
        return "Contact does not exist."
    
    sorted_notes = record.sort_notes_by_tags()
    
    return "\n".join(str(note) for note in sorted_notes)

@input_error
def edit_note_in_contact(args, book: AddressBook):
    if len(args) < 1:
        return "Error: Please provide a contact name."
    
    name = args[0]
    record = book.find(name)
    
    if record is None:
        return "Contact does not exist."
    
    if not record.notes:
        return "This contact has no notes to edit."
    
    for i, note in enumerate(record.notes, start=1):
        tags = ", ".join(note.tags)
        print(f'{i}. {note.title}: {note.content} (Tags: {tags})')
    
    note_number = int(input("Enter the number of the note you want to edit: ").strip())
    if note_number < 1 or note_number > len(record.notes):
        return "Invalid note number."
    
    title = input("Enter new note title (or press Enter to keep the current title): ").strip()
    content = input("Enter new note content (or press Enter to keep the current content): ").strip()
    tags = input("Enter new tags (separated by commas, or press Enter to keep current tags): ").strip().split(',')
    if title:
        record.notes[note_number - 1].title = title
    if content:
        record.notes[note_number - 1].content = content
    if tags:
        record.notes[note_number - 1].tags = [tag.strip() for tag in tags if tag.strip()]
    return "Note edited successfully."

@input_error
def delete_note_from_contact(args, book: AddressBook):
    if len(args) < 1:
        return "Error: Please provide a contact name."
    
    name = args[0]
    record = book.find(name)
    
    if record is None:
        return "Contact does not exist."
    
    if not record.notes:
        return "This contact has no notes to delete."
    
    for i, note in enumerate(record.notes, start=1):
        print(f"{i}. {note.title}: {note.content}")
    
    note_number = int(input("Enter the number of the note you want to delete: ").strip())
    if note_number < 1 or note_number > len(record.notes):
        return "Invalid note number."
    
    record.notes.pop(note_number - 1)
    return "Note deleted successfully."

@input_error
def change_email(args, book: AddressBook):
    name, new_email, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact does not exist."
    record.email = Email(new_email)
    return "Email updated successfully."


@input_error
def delete_email(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact does not exist."
    record.email = None
    return "Email deleted successfully."


@input_error
def change_address(args, book: AddressBook):
    name, new_address, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact does not exist."
    record.address = Address(new_address)
    return "Address updated successfully."


@input_error
def delete_address(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact does not exist."
    record.address = None
    return "Address deleted successfully."

@input_error
def edit_contact_full(args, book: AddressBook):
    if len(args) < 1:
        return "Error: Please provide a contact name."
    
    name = args[0]
    record = book.find(name)
    
    if record is None:
        return "Contact does not exist."
    
    while True:
        print("Select what you want to edit:")
        print("1. Name")
        print("2. Last Name")
        print("3. Phone")
        print("4. Email")
        print("5. Address")
        print("6. Birthday")
        print("7. Notes")
        print("8. Exit")
        
        choice = input("Enter the number: ").strip()

        if choice == '1':
            new_name = input("Enter new name: ").strip()
            for attempt in range(2):
                try:
                    validate_name(new_name)
                    book.data[new_name] = book.data.pop(record.name.value)
                    record.name.value = new_name
                    print("Name updated successfully.")
                    break
                except ValueError as e:
                    if attempt < 1:
                        print(f"Error: {e}. You have {1 - attempt} attempt left.")
                        new_name = input("Re-enter new name: ").strip()
                    else:
                        print(f"Error: {e}. Name not updated.")
        
        elif choice == '2':
            new_last_name = input("Enter new last name: ").strip()
            for attempt in range(2):
                try:
                    validate_name(new_last_name)
                    record.last_name = new_last_name
                    print("Last Name updated successfully.")
                    break
                except ValueError as e:
                    if attempt < 1:
                        print(f"Error: {e}. You have {1 - attempt} attempt left.")
                        new_last_name = input("Re-enter new last name: ").strip()
                    else:
                        print(f"Error: {e}. Last Name not updated.")
        
        elif choice == '3':  # Вибір пункту "Phone"
            while True:
                print("Select an option:")
                print("1. Edit existing phone number")
                print("2. Add new phone number")
                print("3. Back to main menu")

                phone_choice = input("Enter the number: ").strip()

                if phone_choice == '1':
                    if not record.phones:  # Перевірка на порожній список телефонів
                        print("This contact has no phone numbers to edit.")
                        continue
            
                    if len(record.phones) > 1:  # Якщо більше одного номера телефону
                        print("Select the phone number you want to edit:")
                        for i, phone in enumerate(record.phones, start=1):
                            print(f"{i}. {phone.value}")
                        
                        phone_number_choice = int(input("Enter the number of the phone you want to edit: ").strip())
                        
                        if 1 <= phone_number_choice <= len(record.phones):
                            old_phone = record.phones[phone_number_choice - 1].value
                            for attempt in range(2):
                                new_phone = input(f"Enter new phone number to replace {old_phone}: ").strip()
                                try:
                                    validate_phone(new_phone)
                                    record.edit_phone(old_phone, new_phone)
                                    print("Phone number updated successfully.")
                                    break
                                except ValueError as e:
                                    print(f"Error: {e}. You have {1 - attempt} attempts left.")
                            else:
                                print("Phone number not updated.")
                        else:
                            print("Invalid choice. No phone number was edited.")
                    else:  # Якщо лише один номер телефону
                        old_phone = record.phones[0].value
                        for attempt in range(2):
                            new_phone = input(f"Enter new phone number to replace {old_phone}: ").strip()
                            try:
                                validate_phone(new_phone)
                                record.edit_phone(old_phone, new_phone)
                                print("Phone number updated successfully.")
                                break
                            except ValueError as e:
                                print(f"Error: {e}. You have {1 - attempt} attempts left.")
                        else:
                            print("Phone number not updated.")
                
                elif phone_choice == '2':  # Додати новий номер телефону
                    for attempt in range(2):
                        new_phone = input("Enter new phone number: ").strip()
                        try:
                            validate_phone(new_phone)
                            record.add_phone(new_phone)
                            print("New phone number added successfully.")
                            break
                        except ValueError as e:
                            print(f"Error: {e}. You have {1 - attempt} attempts left.")
                    else:
                        print("New phone number not added.")
                
                elif phone_choice == '3':
                    break
                
                else:
                    print("Invalid choice. Please select a valid option.")
        
        elif choice == '4':  # Введення нового email
            for attempt in range(2):
                new_email = input("Enter new email address: ").strip()
                try:
                    record.email = Email(new_email)
                    print("Email updated successfully.")
                    break
                except ValueError as e:
                    print(f"Error: {e}. You have {1 - attempt} attempts left.")
            else:
                print("Email not updated.")
        
        elif choice == '5':
            new_address = input("Enter new address: ").strip()
            record.address = Address(new_address)
            print("Address updated successfully.")
        
        elif choice == '6':
            new_birthday = input("Enter new birthday (DD.MM.YYYY): ").strip()
            record.birthday = Birthday(new_birthday)
            print("Birthday updated successfully.")
        
        elif choice == '7':
            edit_note_in_contact([name], book)
        
        elif choice == '8':
            print("Exiting edit menu.")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")
            
    return "Contact editing completed."

@input_error
def delete_phone(args, book):
    if len(args) < 2:
        return "Error: Please provide a contact name and the phone number to delete."
    name, phone_number, *_ = args
    record = book.find(name)
    
    if record is None:
        return "Contact does not exist."
    
    if not record.find_phone(phone_number):
        return f"{name} does not have this phone number."
    
    record.remove_phone(phone_number)
    return f"Phone number {phone_number} for {name} has been deleted."


@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        return "Error: Please provide a contact name."
    
    name = args[0]
    if book.find(name) is None:
        return "Contact does not exist."
    
    book.delete(name)
    return f"Contact {name} deleted successfully."
