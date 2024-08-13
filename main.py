from models import AddressBook
from utils import parse_input, add_contact, show_contacts, change_contact, get_contact, add_birthday, show_birthday, birthdays
import pickle
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Список доступних команд
COMMANDS = ['hello', 'add', 'change', 'phone', 'all', 'add-birthday', 'show-birthday', 'birthdays', 'close', 'exit', 'q']

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

    book = AddressBook()
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
        elif command == "add":
            print(add_contact(args, book))
        elif command == "all":
            print(show_contacts(book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

    save_data(book)
    
if __name__ == "__main__":
    main()