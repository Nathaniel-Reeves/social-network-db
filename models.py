"""Models module to interact with a sqlite database"""

import sqlite3
import bcrypt

# Define the name of the database and a salt value for password hashing.
DATABASE = 'test.db'
SALT = b'$2b$12$bCkhk/dnjeaHnxqYLh39be'



def valid_user(username, password):
    """Checks if a user with the given username and password exists in the database.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if a user with the given username and password exists, False otherwise.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            people.username,
            people.encrypted_password
        FROM people 
        WHERE people.username = ? ''', (username,))
    result = cursor.fetchone()
    if result is None:
        return False
    conn.close()
    check = bcrypt.checkpw(password.encode("utf-8"), result[1])
    return check

def user_exists(username):
    """Checks if a user with the given username exists in the database.

    Args:
        username (str): The username of the user.

    Returns:
        bool: True if a user with the given username exists, False otherwise.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            people.username
        FROM people 
        WHERE people.username =? ''', (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def create_user(name, username, password):
    """Creates a new user in the database.

        Args:
            name (str): The name of the user.
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            int: The ID of the newly created user.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), SALT)
    result = cursor.execute('''
        INSERT INTO people (name, username, encrypted_password)
        VALUES (?,?,?)''', (name, username, hashed_password))
    conn.commit()
    conn.close()
    return result.lastrowid

def delete_user(username, password):
    """Deletes a user from the database.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if a user with the given username and password exists, False otherwise.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), SALT)
    cursor.execute('''
        DELETE FROM people 
        WHERE people.username =? AND people.encrypted_password =?''', (username, hashed_password))
    conn.commit()
    conn.close()
    return not user_exists(username)

def get_users():
    """Gets all users from the database.

        Returns:
            list: A list of all users.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            people.username,
            people.name
        FROM people 
        ORDER BY people.username''')
    result = cursor.fetchall()
    conn.close()
    return result
