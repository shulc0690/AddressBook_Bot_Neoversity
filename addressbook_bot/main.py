from helper import build_help, commands
from models import AddressBook
from utils import *
import pickle
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style as prompt_style
from special_efects import *

prompt_style = prompt_style.from_dict(
    {
        "prompt": "ansicyan bold",  # prompt style
        "completion-menu.completion": "bg:ansiblack fg:ansigreen",
        "completion-menu.completion.current": "bg:ansiblack fg:ansigreen",
    }
)
list_comands = [command["command"] for command in commands]
command_completer = WordCompleter(list_comands, ignore_case=True)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def header():
    gur_logo = "data/gur_logo.txt"
    with open(gur_logo, "r", encoding="ascii") as fh:
        try:
            header = fh.read()
            logo_style(header)
        except FileNotFoundError:
            error_msg(f"File '{gur_logo}' not found.")
        except IOError:
            error_msg(f"Something went wrong while reading '{gur_logo}'.")


def main():
    book = load_data()
    header()
    session = PromptSession(completer=command_completer)

    info_msg("_____________________________________________\n")
    info_msg("Hello my friend! Welcome to Budanov note bot!\n")
    info_msg('Enter command "help" to see all commands.\n')

    while True:
        user_input = session.prompt(main_msg("Enter a command: "), style=prompt_style)
        if not user_input.strip():
            info_msg("No command entered. Please enter a command.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit", "q"]:
            info_msg("Goodbye, sir! Glory to Ukraine!")
            angry_style("Death to enemies!")
            break
        elif command == "help":
            build_help()
        elif command == "add-contact":
            print(add_contact(args, book))
        elif command == "show-address-book":
            print(show_address_book(book))
        elif command == "edit-phone":
            print(edit_phone(args, book))
        elif command == "show-contact":
            print(get_contact(args, book))
        elif command == "search":
            print(search_contact(args, book))
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
                    error_msg("Please enter a valid number of days.")
            else:
                info_msg("Please specify the number of days.")
        elif command == "add-notes":
            print(add_note_to_contact(args, book))
        elif command == "edit-note":
            print(edit_note_in_contact(args, book))
        elif command == "delete-note":
            print(delete_note_from_contact(args, book))
        elif command == "search-notes-by-tag":
            print(find_notes_by_tag(args, book))
        elif command == "sort-notes-by-tags":
            print(sort_notes_by_tags(args, book))
        elif command == "edit-email":
            print(change_email(args, book))
        elif command == "delete-email":
            print(delete_email(args, book))
        elif command == "edit-address":
            print(change_address(args, book))
        elif command == "delete-address":
            print(delete_address(args, book))
        elif command == "edit-contact":
            print(edit_contact_full(args, book))
        elif command == "edit-birthday":
            print(edit_birthday(args, book))
        elif command == "delete-birthday":
            print(delete_birthday(args, book))
        elif command == "delete-phone":
            print(delete_phone(args, book))
        elif command == "delete-contact":
            print(delete_contact(args, book))
        else:
            error_msg(f'Pardon sir, "{user_input}" command is invalid!')

    save_data(book)


if __name__ == "__main__":
    main()
