"""Main module creates interactions between the user and the models.py module."""

import os
import sys
import models
import getpass


class Session:
    """Creates a new session."""

    def __init__(self, username=""):
        self.username = username

    def login(self, username):
        self.username = username

    def logout(self):
        self.username = ""

    def get_username(self):
        return self.username

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
        if models.user_exists(username):
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

    followers, following = models.get_followers_and_following(current_user_id)

    print("Followers:")
    for follower in followers:
        print(follower)

    print("\nFollowing:")
    for followee in following:
        print(followee)

def add_post(session):
    """Prompts the user for a post and adds it to the database."""
    title = input("What is the title of the post? ")
    content = input("What is the content of the post? ")
    username = session.get_username()
    models.create_post(models.get_user_id(username), title, content)
    print("Post added successfully.")

def remove_post(session):
    """Prompts the user for a post and removes it from the database."""
    id = input("Enter id of post you would like to delete: ")
    models.delete_post(id)
    print("Post deleted successfully.")

def view_feed():
    """Displays all posts."""
    feed = models.fetch_post_feed()
    if feed:
        for post in feed:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"Post ID: {post[0]}")
            print(f"Username: {models.get_username_by_id(post[1])}")
            print(f"Title: {post[2]}")
            print(f"Content: {post[3]}")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def get_most_active_user():
    user = models.get_most_active_user()
    print()
    print("Most active user is:", user)
    print()

def add_comment(session):
    """adds a comment to the database."""
    id = input("Enter id of post you would like to comment on: ")
    username = session.get_username()
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
        print(f"Title: {post[2]}")
        print(f"Content: {post[3]}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Comments:")
        print()
        if post[3]:
            for comment in post[4]:
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
- 3: Unfollow a user
- 4: List friends
- 5: Add post
- 6: Remove post
- 7: View feed
- 8: Add comment
- 9: Remove comment
- 10: View feed with comments
- 11: Get most active user
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
- 5: Get most active user
- 0: Exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

def login_user():
    """Login user."""

    username = input("What is your username? ")
    password = getpass.getpass(prompt="What is your password? ")
    if models.valid_user(username, password):
        print("Welcome back, " + username)
        session = Session(username)
        while True:
            print_user_menu()
            choice = input("What would you like to do? ")
            print()
            if choice == "1":
                print("Goodbye " + username)
                session.logout()
                break
            elif choice == "2":
                add_follower(session)
            elif choice == "3":
                remove_follower(session)
            elif choice == "4":
                list_followers_and_following(session)
            elif choice == "5":
                add_post(session)
            elif choice == "6":
                remove_post(session)
            elif choice == "7":
                view_feed()
            elif choice == "8":
                add_comment(session)
            elif choice == "9":
                remove_comment()
            elif choice == "10":
                view_feed_with_comments()
            elif choice == "11":
                get_most_active_user()
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
        elif choice == "5":
            get_most_active_user()
        elif choice == "0":
            break
        else:
            print('''Invalid option. Please enter the
number corresponding \nto the option you wish to perform.''')
    close()

if __name__ == "__main__":
    main()
