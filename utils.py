from models import AddressBook, Birthday, Record

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
    # Перевірка на те, що введено лише ім'я без додаткового тексту
    if not args or not args[0].strip() or len(args) > 1:
        return "Error: Name must be a single word without spaces. Please provide a valid name."
    name = args[0].strip()
    record = book.find(name)
    message = "Contact updated."
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    # Введення номера телефону з двома спробами
    for i in range(2):
        phone = input("Enter phone number (10 digits) (or press Enter to skip): ").strip()
        if not phone:
            break
        try:
            record.add_phone(phone)
            break
        except ValueError as e:
            print(e)
    else:
        print("Failed to add a valid phone number. Skipping phone.")

    # Введення електронної адреси з двома спробами
    # for i in range(2):
    #     email = input("Enter email address (or press Enter to skip): ").strip()
    #     if not email:
    #         break
    #     try:
    #         record.add_email(email)
    #         break
    #     except ValueError as e:
    #         print(e)
    # else:
    #     print("Failed to add a valid email address. Skipping email.")

    # Введення дати народження з двома спробами
    for i in range(2):
        birthday = input("Enter birthday (DD.MM.YYYY) (or press Enter to skip): ").strip()
        if not birthday:
            break
        try:
            record.add_birthday(birthday)
            break
        except ValueError as e:
            print(e)
    else:
        print("Failed to add a valid birthday. Skipping birthday.")

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