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
            list: A list of all users tuples.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            people._id,
            people.username,
            people.name
        FROM people 
        ORDER BY people.username''')
    result = cursor.fetchall()
    conn.close()
    return result

def add_comment(post_id, content):
    """Adds a comment to the database.

        Args:
            post_id (int): The id of the post being commmented on.
            content (str): The content of the comment.

        Returns:
            str: Comment added
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if post with given ID exists
    cursor.execute('SELECT * FROM posts WHERE _id = ?', (post_id,))
    post = cursor.fetchone()
    if not post:
        return None  # Return None if post with given ID does not exist

    # Insert new comment into comments table
    cursor.execute('INSERT INTO comments (post_id, content) VALUES (?, ?)',
                   (post_id, content))
    conn.commit()

    # Get ID of new comment
    comment_id = cursor.lastrowid

    # Fetch newly created comment
    cursor.execute('SELECT * FROM comments WHERE _id = ?', (comment_id,))
    comment = cursor.fetchone()

    # Close database connection and return newly created comment
    conn.close()
    return comment


def remove_comment(comment_id):
    """removes a comment from the database.

        Args:
            comment_id (int): The id of the comment being deleted.

        Returns:
            bool: If comment was deleted
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Delete the comment with the given ID
    cursor.execute("DELETE FROM comments WHERE id=?", (comment_id,))
    conn.commit()

    # Close the connection and return success
    conn.close()
    return True

def get_all_posts_with_comments():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # get all posts
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()

    # get all comments for each post
    for i, post in enumerate(posts):
        cursor.execute("SELECT * FROM comments WHERE post_id=?", (post[0],))
        comments = cursor.fetchall()
        posts[i] = (post, comments)

    conn.close()
    return posts
