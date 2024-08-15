from models import AddressBook, Birthday, Record, Email, Address


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
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

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
def change_contact(args, book: AddressBook):
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
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact does not exists."
    return record


def show_contacts(book: AddressBook):
    """Function returns all contacts."""
    if len(book) == 0:
        return "Contact list is empty."
    return book


@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    message = "Birthday added."
    if record is None:
        return "Contact does not exists."
    if birthday:
        record.add_birthday(Birthday(birthday))
    return message


@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact does not exists."
    return record.birthday.value.strftime('%d.%m.%Y')


@input_error
def birthdays(book):
    return book.get_upcoming_birthdays()

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

    record.add_note(title, content)
    return "Note added successfully."

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
        print(f"{i}. {note.title}: {note.content}")
    
    note_number = int(input("Enter the number of the note you want to edit: ").strip())
    if note_number < 1 or note_number > len(record.notes):
        return "Invalid note number."
    
    title = input("Enter new note title (or press Enter to keep the current title): ").strip()
    content = input("Enter new note content (or press Enter to keep the current content): ").strip()
    
    if title:
        record.notes[note_number - 1].title = title
    if content:
        record.notes[note_number - 1].content = content
    
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