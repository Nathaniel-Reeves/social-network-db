"""Main module creates interactions between the user and the models.py module."""

import os
import sys
import models

def welcome():
    """Prints the welcome message."""
    welcome_message = """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Welcome to Social Network!
This is a simple social network application created for
a CS-4307 Database Systems course at Utah Tech University by
Nathaniel Reeves and Marie Sewell on 2/20/2023.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
    print(welcome_message)

def close():
    """Closes the program."""
    print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            Goodbye!
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
    sys.exit()

def add_user():
    """Adds a new user to the database."""
    name = input("What is your first and last name? ")
    while True:
        username = input("What is your username? ")
        if models.user_exists(username):
            print("That username is already in use.")
        else:
            break
    password = input("What is your password? ", password=True)
    _id = models.create_user(name, username, password)
    if _id:
        print(f"User {username} has been added.")
    else:
        print("Something went wrong. Try again.")

def remove_user():
    """Removes a user from the database."""
    while True:
        username = input("What is your username? ")
        if not models.user_exists(username):
            break
        print("That username does not exist.")
    password = input("What is your password? ", password=True)
    if models.delete_user(username, password):
        print(f"User {username} has been removed.")
    else:
        print("Something went wrong. Try again.")

def list_users():
    """Lists all users in the database."""
    users = models.get_users()
    if users:
        for user in users:
            print("Name: '{:<20}Username: '{:<20}".format(user[2] + "',", user[1] + "'."))

def add_follower():
    # TODO: Add a follower to the database
    pass

def remove_follower():
    # TODO: Remove a follower from the database
    pass

def list_followers():
    # TODO: List all followers in the database
    pass

def add_post():
    # TODO: Add a post to the database
    pass

def remove_post():
    # TODO: Remove a post from the database
    pass

def view_feed():
    # TODO: List all posts in the database
    pass

def add_comment():
    # TODO: Add a comment to the database
    pass

def remove_comment():
    # TODO: Remove a comment from the database
    pass

def view_feed_with_comments():
    # TODO: List all posts with comments in the database
    pass

def print_user_menu():
    """Prints the user's menu."""
    print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
User Menu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Options:
- 1: Logout
- 2: Add follower
- 3: Remove follower
- 4: List followers
- 5: Add post
- 6: Remove post
- 7: View feed
- 8: Add comment
- 9: Remove comment
- 10: View feed with comments
- 0: Exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

def print_main_menu():
    """Prints the main menu."""
    print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Main Menu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Options:
- 1: Add a user
- 2: Remove a user
- 3: List all users
- 4: Login user
- 0: Exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

def login_user():
    """Login user."""

    username = input("What is your username? ")
    password = input("What is your password? ", password=True)
    if models.valid_user(username, password):
        print("Welcome back, " + username)
        while True:
            print_user_menu()
            choice = input("What would you like to do? ")
            print()
            if choice == "1":
                print("Goodbye " + username)
                break
            elif choice == "2":
                add_follower()
            elif choice == "3":
                remove_follower()
            elif choice == "4":
                list_followers()
            elif choice == "5":
                add_post()
            elif choice == "6":
                remove_post()
            elif choice == "7":
                view_feed()
            elif choice == "8":
                add_comment()
            elif choice == "9":
                remove_comment()
            elif choice == "10":
                view_feed_with_comments()
            elif choice == "0":
                close()
            else:
                print('''Invalid option. Please enter the
number corresponding \nto the option you wish to perform.''')
    else:
        print("Invalid username or password.")

def main():
    """The main function creates the user interface."""

    file_name = "test.db"
    if not os.path.exists(file_name):
        import init_db
        init_db.main()

    welcome()
    while True:
        print_main_menu()
        choice = input("What would you like to do? ")
        print()
        if choice == "1":
            add_user()
        elif choice == "2":
            remove_user()
        elif choice == "3":
            list_users()
        elif choice == "4":
            login_user()
        elif choice == "0":
            break
        else:
            print('''Invalid option. Please enter the
number corresponding \nto the option you wish to perform.''')
    close()

if __name__ == "__main__":
    main()
