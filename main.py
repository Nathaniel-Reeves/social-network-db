"""Main module creates interactions between the user and the models.py module."""

import os
import sys
import models
import getpass

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
    password = getpass.getpass(prompt="What is your password? ")
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
    password = getpass.getpass(prompt="What is your password? ")
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

def add_follower(session):
    follower_username = session.get_username()
    
    followee_username = input("Enter the username of the friend you would like to add: ")
    
    follower_id = models.get_user_id(follower_username)
    followee_id = models.get_user_id(followee_username)
    
    if not follower_id or not followee_id:
        print("Error: Invalid username entered.")
        return
    
    result = models.add_follower(follower_id, followee_id)
    
    if result:
        print("Follower added successfully.")
    else:
        print("Error: Unable to add follower.")

def remove_follower(session):
    """Prompts the user for follower and followed user IDs and removes follower."""
    follower_username = session.get_username()
    
    followee_username = input("Enter the username of the friend to remove: ")

    follower_id = models.get_user_id(follower_username)
    followee_id = models.get_user_id(followee_username)

    message = models.remove_follower(follower_id, followee_id)
    print(message)

def list_followers_and_following(session):
    """List the current user's followers and users they are following."""
    current_user_id = models.get_user_id(session.get_username())
=======
def add_follower():
    # TODO: Add a follower to the database
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
    """adds a comment to the database."""
    id = input("Enter id of post you would like to comment on: ")
    username = input("Enter your username: ")
    comment = input("Enter comment: ")
    models.add_comment(id, models.get_user_id(username), comment)
    

def remove_comment():
    """deletes a comment from the database."""
    id = input("Enter id of comment you would like to delete: ")
    models.remove_comment(id)

def view_feed_with_comments():
    """Displays all posts and their comments."""
    feed = models.get_feed_with_comments()

    for post in feed:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"Post ID: {post[0]}")
        print(f"Username: {models.get_username_by_id(post[1])}")
        print(f"Content: {post[2]}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Comments:")
        print()
        if post[3]:
            for comment in post[3]:
                print(f"Comment ID: {comment[0]}")
                print(f"Username: {models.get_username_by_id(comment[1])}")
                print(f"Content: {comment[2]}")
                print()
        else:
            print("No comments.")

        print("\n")


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
- 5: List following
- 6: Add post
- 7: Remove post
- 8: View feed
- 9: Add comment
- 10: Remove comment
- 11: View feed with comments
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
    password = getpass.getpass(prompt="What is your password? ")
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
                list_following()
            elif choice == "6":
                add_post()
            elif choice == "7":
                remove_post()
            elif choice == "8":
                view_feed()
            elif choice == "9":
                add_comment()
            elif choice == "10":
                remove_comment()
            elif choice == "11":
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
