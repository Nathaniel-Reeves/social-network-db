import os
import sys
import models

def welcome():
    welcome_message = """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Welcome to Social Network!
This is a simple social network application created for
a CS-4307 Database Systems course at Utah Tech University by
Nathaniel Reeves and Marie Sewell on 2/20/2023.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
    print(welcome_message)
    print()

def close():
    print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        Goodbye!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""")
    sys.exit()

def add_user():
    # TODO: Add a user to the database
    pass

def remove_user():
    # TODO: Remove a user from the database
    pass

def list_users():
    # TODO: List all users in the database
    pass

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
    # TODO: Print the user menu
    pass

def print_main_menu():
    # TODO: Print the main menu
    pass
          
def login_user():
    username = input("What is your username? ")
    password = input("What is your password? ")
    if models.valid_user(username, password):
        print("Welcome back, " + username)
        while True:
            print_user_menu()
            choice = input("What would you like to do? ")
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
        print("Invalid username or password.")

def main():
    file_name = "test.db"
    if not os.path.exists(file_name):
        import init_db
        init_db.main()

    welcome()
    while True:
        print_main_menu()
        choice = input("What would you like to do? ")
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
    close()

if __name__ == "__main__":
    main()