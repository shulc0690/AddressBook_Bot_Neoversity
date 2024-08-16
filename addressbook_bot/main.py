from addressbook_bot.models import AddressBook
from addressbook_bot.utils import *
import pickle
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Список доступних команд
COMMANDS = ['hello', 'add-contact', 'edit-phone', 'edit-contact', 'show-contact', 'show-address-book',
            'add-birthday', 'show-birthday', 'add-notes', 'edit-note', 'delete-note', 'birthdays', 
            'change-email', 'delete-email', 'change-address', 'delete-address','find-notes-by-tag', 'sort-notes-by-tags', 'close', 'exit', 'q']


# Автозаповнення команд
command_completer = WordCompleter(COMMANDS, ignore_case=True)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, 'wb') as file:
        pickle.dump(book, file)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    
    session = PromptSession(completer=command_completer)

    print("It's alive! It's alive!")

    while True:
        user_input = session.prompt("Enter a command: ")
        if not user_input.strip():
            print("No command entered. Please enter a command.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit", "q"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add-contact":
            print(add_contact(args, book))
        elif command == "show-address-book":
            print(show_address_book(book))
        elif command == "edit-phone":
            print(edit_contact(args, book))
        elif command == "show-contact":
            print(get_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            if args:
                try:
                    days = int(args[0])
                    print(birthdays(book, days))
                except ValueError:
                    print("Please enter a valid number of days.")
            else:
                print("Please specify the number of days.")
        elif command == "add-notes":
            print(add_note_to_contact(args, book))
        elif command == "edit-note":
            print(edit_note_in_contact(args, book))
        elif command == "delete-note":
            print(delete_note_from_contact(args, book))
        elif command == "find-notes-by-tag":
            print(find_notes_by_tag(args, book))
        elif command == "sort-notes-by-tags":
            print(sort_notes_by_tags(args, book))    
        elif command == "change-email":
            print(change_email(args, book))
        elif command == "delete-email":
            print(delete_email(args, book))
        elif command == "change-address":
            print(change_address(args, book))
        elif command == "delete-address":
            print(delete_address(args, book))
        elif command == "edit-contact":
            print(edit_contact_full(args, book))
        else:
            print("Invalid command.")

    save_data(book)


if __name__ == "__main__":
    main()
