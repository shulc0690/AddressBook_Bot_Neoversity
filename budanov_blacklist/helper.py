from budanov_blacklist.special_efects import *
# Список доступних команд
commands = [
    {
        "command": "add-contact",
        "description": "Add contact",
        "syntax": "add-contact <name>",
        "example": "add-contact John",
        "object": "contact",
    },
    {
        "command": "delete-contact",
        "description": "Delete contact",
        "syntax": "delete-contact <name>",
        "example": "delete-contact John",
        "object": "contact",
    },
    {
        "command": "edit-contact",
        "description": "Edit contact",
        "syntax": "edit-contact <name>",
        "example": "edit-contact John",
        "object": "contact",
    },
    {
        "command": "show-contact",
        "description": "Display contact",
        "syntax": "show-contact <name>",
        "example": "show-contact John",
        "object": "contact",
    },
    {
        "command": "edit-phone",
        "description": "Edit phone number of contact",
        "syntax": "edit-phone <name>",
        "example": "edit-phone John",
        "object": "phone",
    },
    {
        "command": "delete-phone",
        "description": "Delete phone number from contact",
        "syntax": "delete-phone <name>",
        "example": "delete-phone John",
        "object": "phone",
    },
    {
        "command": "show-address-book",
        "description": "Display all list of contacts",
        "syntax": "show-address-book",
        "example": "show-address-book",
        "object": "address-book",
    },
    {
        "command": "search",
        "description": "Search contact by all properties",
        "syntax": "search <keyword>",
        "example": "search 2024",
        "object": "address-book",
    },
    {
        "command": "add-birthday",
        "description": "Add birthday to contact",
        "syntax": "add-birthday <name> <birthday>",
        "example": "add-birthday John 08.08.1991",
        "object": "birthday",
    },
    {
        "command": "show-birthday",
        "description": "Display birthday of contact",
        "syntax": "show-birthday <name>",
        "example": "show-birthday John",
        "object": "birthday",
    },
    {
        "command": "edit-birthday",
        "description": "Edit birthday of contact",
        "syntax": "edit-birthday <name> <birthday>",
        "example": "edit-birthday John 08.08.1991",
        "object": "birthday",
    },
    {
        "command": "delete-birthday",
        "description": "Delete birthday of contact",
        "syntax": "delete-birthday <name>",
        "example": "delete-birthday John",
        "object": "birthday",
    },
    {
        "command": "birthdays",
        "description": "Display a list of contacts whose birthday is a specified number of days from the current date",
        "syntax": "birthdays <days>",
        "example": "birthdays 7",
        "object": "birthday",
    },
    {
        "command": "add-notes",
        "description": "Add notes to contact",
        "syntax": "add-notes <name>",
        "example": "add-notes John",
        "object": "notes",
    },
    {
        "command": "edit-note",
        "description": "Edit note of contact",
        "syntax": "edit-note <name>",
        "example": "edit-note John",
        "object": "notes",
    },
    {
        "command": "delete-note",
        "description": "Delete note of contact",
        "syntax": "delete-note <name>",
        "example": "delete-note John",
        "object": "notes",
    },
    {
        "command": "search-notes-by-tag",
        "description": "Search notes in contact by tag",
        "syntax": "search-notes-by-tag <name> <tag>",
        "example": "search-notes-by-tag John",
        "object": "notes",
    },
    {
        "command": "sort-notes-by-tags",
        "description": "Sort notes in contact by tag",
        "syntax": "sort-notes-by-tags <name>",
        "example": "sort-notes-by-tags John",
        "object": "notes",
    },
    {
        "command": "edit-email",
        "description": "Edit email of contact",
        "syntax": "edit-email <name> <email>",
        "example": "edit-email John john@gmail.com",
        "object": "email",
    },
    {
        "command": "delete-email",
        "description": "Delete email of contact",
        "syntax": "delete-email <name>",
        "example": "delete-email John",
        "object": "email",
    },
    {
        "command": "edit-address",
        "description": "Edit address of contact",
        "syntax": "edit-address <name> <address>",
        "example": "edit-address John john@gmail.com",
        "object": "address",
    },
    {
        "command": "delete-address",
        "description": "Delete address of contact",
        "syntax": "delete-address <name>",
        "example": "delete-address John",
        "object": "address",
    },
]


def build_help():
    main_msg(f"Commands:")
    section = ""
    for command in commands:
        if section != command["object"]:
            main_msg(f"  {command['object']}")
        main_msg(f"      {command['syntax']:<60}{command['description']:<60}")
        section = command["object"]
