from models import AddressBook, Birthday, Record, Email, Address
import re
from datetime import datetime, timedelta
from special_efects import *
from rich.console import Console
from rich.table import Table

console = Console()


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
    if re.fullmatch(r"\d{10}", phone):
        return True
    else:
        combed_msg = error_msg4return("Phone number must contain exactly 10 digits.")
        raise ValueError(combed_msg)


def validate_name(name):
    """Validates that the name or last name contains only letters and is a single word."""
    if re.fullmatch(r"[A-Za-zА-Яа-яЇїІіЄєҐґ]+", name):
        return True
    else:
        combed_msg = error_msg4return(
            "Name and Last Name must contain only letters and be a single word."
        )
        raise ValueError(combed_msg)


@input_error
def parse_input(user_input):
    """Function parses input."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    if not args or not args[0].strip() or len(args) > 1:
        combed_msg = error_msg4return(
            "Error: Name must be a single word without spaces. Please provide a valid name."
        )
        return combed_msg
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
    combed_msg = info_msg4return("Enter last name (or press Enter to skip): ")
    last_name = input(combed_msg).strip()
    for attempt in range(2):
        if last_name:
            try:
                validate_name(last_name)
                record.last_name = last_name
                break
            except ValueError as e:
                if attempt < 1:
                    error_msg(f"Error: {e}. You have {1 - attempt} attempt left.")
                    last_name = input(main_msg4return("Re-enter last name: ")).strip()
                else:
                    error_msg(f"Error: {e}. Last Name not added.")

    for i in range(2):
        combed_msg = info_msg4return(
            "Enter phone number (10 digits) (or press Enter to skip): "
        )
        phone = input(combed_msg).strip()
        if not phone:
            break
        try:
            record.add_phone(phone)
            break
        except ValueError as e:
            print(e)

    for i in range(2):
        combed_msg = info_msg4return("Enter email address (or press Enter to skip): ")
        email = input(combed_msg).strip()
        if not email:
            break
        try:
            record.add_email(email)
            break
        except ValueError as e:
            print(e)

    for i in range(2):
        combed_msg = info_msg4return("Enter address (or press Enter to skip): ")
        address = input(combed_msg).strip()
        if not address:
            break
        record.add_address(address)
        break

    for i in range(2):
        combed_msg = info_msg4return(
            "Enter birthday (DD.MM.YYYY) (or press Enter to skip): "
        )
        birthday = input(combed_msg).strip()
        if not birthday:
            break
        try:
            record.add_birthday(birthday)
            break
        except ValueError as e:
            print(e)
    combed_msg = info_msg4return(message)
    return combed_msg


@input_error
def edit_phone(args, book: AddressBook):
    """Function changes existing contact."""
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = "Phone updated."

    if record is None:
        message = "Contact does not exists."
    if new_phone and old_phone:
        record.edit_phone(old_phone, new_phone)

    combed_msg = info_msg4return(message)
    return combed_msg


@input_error
def get_contact(args, book: AddressBook):
    """Function get phone for existing contact."""
    if len(args) < 1:
        combed_msg = error_msg4return("Error: Please provide a contact name.")
        return combed_msg
    name, *_ = args
    record = book.find(name)
    if record is None:
        return info_msg4return("Contact does not exist.")
    return record


@input_error
def search_contact(args, book: AddressBook):
    """Function search contact by all fields."""
    if len(args) < 1:
        combed_msg = error_msg4return("Error: Please provide a keyword.")
        return combed_msg
    keyword, *_ = args
    records = book.search(keyword)
    if records is None:
        combed_msg = info_msg4return(
            "There is no contact that matches the search data."
        )
        return combed_msg
    return print_contacts_table(records)


def print_contacts_table(book):
    table = Table(
        title="BUDANOV BLACK LIST",
        show_lines=True,
        title_style="green",
        border_style="green",
    )
    table.add_column("Name", style="cyan", no_wrap=True, header_style="green")
    table.add_column("Last Name", style="cyan", header_style="green")
    table.add_column("Phone", style="green", header_style="green")
    table.add_column("Email", style="cyan", header_style="green")
    table.add_column("Address", style="blue", header_style="green")
    table.add_column("Birthday", style="yellow", header_style="green")
    table.add_column("Notes", style="bright_black", header_style="green")
    for record in book.data.values():
        last_name_str = record.last_name if record.last_name else "No last name"
        phones_str = (
            "; ".join(p.value for p in record.phones) if record.phones else "No phone"
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
            birthday_str = "Alive yet"
        notes_str = "\n".join(
            f"{i+1}. {note.title}: {note.content}"
            for i, note in enumerate(record.notes)
        )
        if not notes_str:
            notes_str = "No notes"
        table.add_row(
            record.name.value,
            last_name_str,
            phones_str,
            email_str,
            address_str,
            birthday_str,
            notes_str,
        )
    console.print(table)


def show_address_book(book: AddressBook):
    """Function returns all contacts."""
    if len(book) == 0:
        combed_msg = info_msg4return("Contact list is empty.")
        return combed_msg
    return print_contacts_table(book)


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Error: Please provide a contact name and a birthday."
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(name=name)
        book.add_record(record)
        message = f"Contact '{name}' created."
    else:
        message = "Contact found."
    try:
        birthday = Birthday(birthday_str)
        record.add_birthday(birthday.value.strftime("%d.%m.%Y"))
        return f"{message} Birthday added."
    except ValueError as e:
        return f"Error: {e}"


@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return info_msg4return("Contact does not exist.")
    return record.birthday.value.strftime("%d.%m.%Y")


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
        return error_msg4return("Error: Please provide a contact name.")
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
                    {
                        "name": record.name.value,
                        "birthday": birthday.strftime("%d.%m.%Y"),
                    }
                )

    if not upcoming_birthdays:
        return info_msg4return(f"No birthdays within the next {days} days.")

    result = f"Birthdays within the next {days} days:\n"
    for entry in upcoming_birthdays:
        result += f"- {entry['name']} on {entry['birthday']}\n"
    return result.strip()


@input_error
def add_note_to_contact(args, book: AddressBook):
    if len(args) < 1:
        combed_msg = error_msg4return("Error: Please provide a contact name.")
        return combed_msg

    name = args[0]
    record = book.find(name)

    if record is None:
        return info_msg4return("Contact does not exist.")

    title = input(main_msg4return("Enter note title: ")).strip()
    content = input(main_msg4return("Enter note content: ")).strip()
    tags = (
        input(main_msg4return("Enter tags (separated by commas):")).strip().split(",")
    )
    record.add_note(title, content)
    record.notes[-1].add_tags([tag.strip() for tag in tags if tag.strip()])
    return info_msg4return("Note added successfully.")


def find_notes_by_tag(args, book: AddressBook):
    if len(args) < 2:
        combed_msg = error_msg4return("Error: Please provide a contact name and a tag.")
        return combed_msg

    name = args[0]
    tag = args[1]
    record = book.find(name)

    if record is None:
        return info_msg4return("Contact does not exist.")

    matching_notes = record.find_notes_by_tag(tag)

    if isinstance(matching_notes, str):
        return matching_notes

    return "\n".join(str(note) for note in matching_notes)


@input_error
def sort_notes_by_tags(args, book: AddressBook):
    if len(args) < 1:
        combed_msg = error_msg4return("Error: Please provide a contact name.")
        return combed_msg

    name = args[0]
    record = book.find(name)

    if record is None:
        return info_msg4return("Contact does not exist.")

    sorted_notes = record.sort_notes_by_tags()

    return "\n".join(str(note) for note in sorted_notes)


@input_error
def edit_note_in_contact(args, book: AddressBook):
    if len(args) < 1:
        combed_msg = error_msg4return("Error: Please provide a contact name.")
        return combed_msg

    name = args[0]
    record = book.find(name)

    if record is None:
        return info_msg4return("Contact does not exist.")

    if not record.notes:
        combed_msg = info_msg4return("This contact has no notes to edit.")
        return combed_msg

    for i, note in enumerate(record.notes, start=1):
        tags = ", ".join(note.tags)
        print(f"{i}. {note.title}: {note.content} (Tags: {tags})")

    note_number = int(
        input(
            main_msg4return("Enter the number of the note you want to edit: ")
        ).strip()
    )
    if note_number < 1 or note_number > len(record.notes):
        combed_msg = info_msg4return("Invalid note number.")
        return combed_msg

    title = input(
        main_msg4return(
            "Enter new note title (or press Enter to keep the current title): "
        )
    ).strip()
    content = input(
        main_msg4return(
            "Enter new note content (or press Enter to keep the current content): "
        )
    ).strip()
    tags = (
        input(
            main_msg4return(
                "Enter new tags (separated by commas, or press Enter to keep current tags): "
            )
        )
        .strip()
        .split(",")
    )
    if title:
        record.notes[note_number - 1].title = title
    if content:
        record.notes[note_number - 1].content = content
    if tags:
        record.notes[note_number - 1].tags = [
            tag.strip() for tag in tags if tag.strip()
        ]
    combed_msg = info_msg4return("Note edited successfully.")
    return combed_msg


@input_error
def delete_note_from_contact(args, book: AddressBook):
    if len(args) < 1:
        combed_msg = error_msg4return("Error: Please provide a contact name.")
        return combed_msg

    name = args[0]
    record = book.find(name)

    if record is None:
        return info_msg4return("Contact does not exist.")

    if not record.notes:
        combed_msg = info_msg4return("This contact has no notes to delete.")
        return combed_msg

    for i, note in enumerate(record.notes, start=1):
        info_msg(f"{i}. {note.title}: {note.content}")

    note_number = int(
        input(
            info_msg4return("Enter the number of the note you want to delete: ")
        ).strip()
    )
    if note_number < 1 or note_number > len(record.notes):
        combed_msg = info_msg4return("Invalid note number.")
        return combed_msg

    record.notes.pop(note_number - 1)
    combed_msg = info_msg4return("Note deleted successfully.")
    return combed_msg


@input_error
def change_email(args, book: AddressBook):
    name, new_email, *_ = args
    record = book.find(name)
    if record is None:
        return info_msg4return("Contact does not exist.")
    record.email = Email(new_email)
    combed_msg = info_msg4return("Email updated successfully.")
    return combed_msg


@input_error
def delete_email(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return info_msg4return("Contact does not exist.")
    record.email = None
    combed_msg = info_msg4return("Email deleted successfully.")
    return combed_msg


@input_error
def change_address(args, book: AddressBook):
    name, new_address, *_ = args
    record = book.find(name)
    if record is None:
        return info_msg4return("Contact does not exist.")
    record.address = Address(new_address)
    combed_msg = info_msg4return("Address updated successfully.")
    return combed_msg


@input_error
def delete_address(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return info_msg4return("Contact does not exist.")
    record.address = None
    return "Address deleted successfully."


@input_error
def edit_contact_full(args, book: AddressBook):
    if len(args) < 1:
        return error_msg4return("Error: Please provide a contact name.")

    name = args[0]
    record = book.find(name)

    if record is None:
        return "Contact does not exist."

    while True:
        main_msg("Select what you want to edit:")
        main_msg("1. Name")
        main_msg("2. Last Name")
        main_msg("3. Phone")
        main_msg("4. Email")
        main_msg("5. Address")
        main_msg("6. Birthday")
        main_msg("7. Notes")
        main_msg("8. Exit")

        choice = input(main_msg4return("Enter the number: ")).strip()

        if choice == "1":
            new_name = input(main_msg4return("Enter new name: ")).strip()
            for attempt in range(2):
                try:
                    validate_name(new_name)
                    book.data[new_name] = book.data.pop(record.name.value)
                    record.name.value = new_name
                    info_msg("Name updated successfully.")
                    break
                except ValueError as e:
                    if attempt < 1:
                        error_msg(f"Error: {e}. You have {1 - attempt} attempt left.")
                        new_name = input(info_msg4return("Re-enter new name: ")).strip()
                    else:
                        error_msg(f"Error: {e}. Name not updated.")

        elif choice == "2":
            new_last_name = input(main_msg4return("Enter new last name: ")).strip()
            for attempt in range(2):
                try:
                    validate_name(new_last_name)
                    record.last_name = new_last_name
                    info_msg("Last Name updated successfully.")
                    break
                except ValueError as e:
                    if attempt < 1:
                        error_msg(f"Error: {e}. You have {1 - attempt} attempt left.")
                        new_last_name = input(
                            info_msg4return("Re-enter new last name: ")
                        ).strip()
                    else:
                        error_msg(f"Error: {e}. Last Name not updated.")

        elif choice == "3":  # Вибір пункту "Phone"
            while True:
                main_msg("Select an option:")
                main_msg("1. Edit existing phone number")
                main_msg("2. Add new phone number")
                main_msg("3. Back to main menu")

                phone_choice = input(main_msg4return("Enter the number: ")).strip()

                if phone_choice == "1":
                    if not record.phones:  # Перевірка на порожній список телефонів
                        info_msg("This contact has no phone numbers to edit.")
                        continue

                    if len(record.phones) > 1:  # Якщо більше одного номера телефону
                        main_msg("Select the phone number you want to edit:")
                        for i, phone in enumerate(record.phones, start=1):
                            main_msg(f"{i}. {phone.value}")

                        phone_number_choice = int(
                            input(
                                main_msg4return(
                                    "Enter the number of the phone you want to edit: "
                                )
                            ).strip()
                        )

                        if 1 <= phone_number_choice <= len(record.phones):
                            old_phone = record.phones[phone_number_choice - 1].value
                            for attempt in range(2):
                                new_phone = input(
                                    main_msg4return(
                                        f"Enter new phone number to replace {old_phone}: "
                                    )
                                ).strip()
                                try:
                                    validate_phone(new_phone)
                                    record.edit_phone(old_phone, new_phone)
                                    info_msg("Phone number updated successfully.")
                                    break
                                except ValueError as e:
                                    error_msg(
                                        f"Error: {e}. You have {1 - attempt} attempts left."
                                    )
                            else:
                                info_msg("Phone number not updated.")
                        else:
                            info_msg("Invalid choice. No phone number was edited.")
                    else:  # Якщо лише один номер телефону
                        old_phone = record.phones[0].value
                        for attempt in range(2):
                            new_phone = input(
                                main_msg4return(
                                    f"Enter new phone number to replace {old_phone}: "
                                )
                            ).strip()
                            try:
                                validate_phone(new_phone)
                                record.edit_phone(old_phone, new_phone)
                                info_msg("Phone number updated successfully.")
                                break
                            except ValueError as e:
                                print(
                                    f"Error: {e}. You have {1 - attempt} attempts left."
                                )
                        else:
                            info_msg("Phone number not updated.")

                elif phone_choice == "2":  # Додати новий номер телефону
                    for attempt in range(2):
                        new_phone = input(
                            main_msg4return("Enter new phone number: ")
                        ).strip()
                        try:
                            validate_phone(new_phone)
                            record.add_phone(new_phone)
                            info_msg("New phone number added successfully.")
                            break
                        except ValueError as e:
                            error_msg(
                                f"Error: {e}. You have {1 - attempt} attempts left."
                            )
                    else:
                        info_msg("New phone number not added.")

                elif phone_choice == "3":
                    break

                else:
                    info_msg("Invalid choice. Please select a valid option.")

        elif choice == "4":  # Введення нового email
            for attempt in range(2):
                new_email = input(info_msg4return("Enter new email address: ")).strip()
                try:
                    record.email = Email(new_email)
                    info_msg("Email updated successfully.")
                    break
                except ValueError as e:
                    error_msg(f"Error: {e}. You have {1 - attempt} attempts left.")
            else:
                info_msg("Email not updated.")

        elif choice == "5":
            new_address = input(info_msg4return("Enter new address: ")).strip()
            record.address = Address(new_address)
            info_msg("Address updated successfully.")

        elif choice == "6":
            new_birthday = input(
                info_msg4return("Enter new birthday (DD.MM.YYYY): ")
            ).strip()
            record.birthday = Birthday(new_birthday)
            info_msg("Birthday updated successfully.")

        elif choice == "7":
            edit_note_in_contact([name], book)

        elif choice == "8":
            info_msg("Exiting edit menu.")
            break

        else:
            info_msg("Invalid choice. Please select a valid option.")

    return info_msg4return("Contact editing completed.")


@input_error
def delete_phone(args, book):
    if len(args) < 2:
        return error_msg4return(
            "Error: Please provide a contact name and the phone number to delete."
        )
    name, phone_number, *_ = args
    record = book.find(name)

    if record is None:
        return info_msg4return("Contact does not exist.")

    if not record.find_phone(phone_number):
        return info_msg4return(f"{name} does not have this phone number.")

    record.remove_phone(phone_number)
    return info_msg4return(f"Phone number {phone_number} for {name} has been deleted.")


@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        return error_msg4return("Error: Please provide a contact name.")

    name = args[0]
    if book.find(name) is None:
        return info_msg4return("Contact does not exist.")

    book.delete(name)
    return info_msg4return(f"Contact {name} deleted successfully.")
