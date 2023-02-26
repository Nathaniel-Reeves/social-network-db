"""Models module to interact with a sqlite database"""

import sqlite3
import bcrypt
from datetime import datetime

# Define the name of the database and a salt value for password hashing.
if __name__ == '__main__':
    DATABASE = 'social_media.db'
else:
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

def get_user_id(username):
    """Returns the id of the user with the given username.

    Args:
        username (str): The username of the user.

    Returns:
        int: The id of the user.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Retrieve the id of the user with the given username
    cursor.execute('SELECT _id FROM people WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row:
        user_id = row[0]
    else:
        user_id = None

    # Close the database connection and return the user ID
    conn.close()
    return user_id

def get_username_by_id(user_id):
    """Returns the username of a user given their ID.

    Args:
        user_id (int): The ID of the user to lookup.

    Returns:
        str: The username of the user.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT username FROM people WHERE _id = ?', (user_id,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None

def get_comments_by_post_id(post_id):
    """Fetches all comments for a given post from the database.

    Args:
        post_id (int): The id of the post for which to fetch comments.

    Returns:
        list of dict: A list of dictionaries, where each dictionary represents a comment.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch comments for given post ID
    cursor.execute('SELECT * FROM comments WHERE post_id = ?', (post_id,))
    comments = cursor.fetchall()

    # Close database connection and return comments
    conn.close()
    return comments


def add_comment(post_id, author_id, content):
    """Adds a comment to the database.

    Args:
        post_id (int): The id of the post being commented on.
        author_id (int): The id of the user adding the comment.
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
    
    # Check if user with given ID exists
    cursor.execute('SELECT * FROM people WHERE _id =?', (author_id,))
    user = cursor.fetchone()
    if not user:
        return None  # Return None if user with given ID does not exist

    # Insert new comment into comments table
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO comments (post_id, author_id, content, timestamp) VALUES (?, ?, ?, ?)',
                   (post_id, author_id, content, timestamp))
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
    cursor.execute("DELETE FROM comments WHERE _id=?", (comment_id,))
    conn.commit()

    # Close the connection and return success
    changes = conn.total_changes
    conn.close()
    return not not changes

def get_feed_with_comments():
    """Returns all posts and their associated comments."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Join posts and comments tables
    cursor.execute('SELECT posts._id, posts.author_id, posts.title, posts.content, comments._id, comments.author_id, comments.content '
                   'FROM posts LEFT JOIN comments ON posts._id = comments.post_id')

    # Group results by post ID to combine posts with their comments
    results = cursor.fetchall()
    feed = {}
    for row in results:
        post_id = row[0]
        if post_id not in feed:
            feed[post_id] = (row[0], row[1], row[2], row[3], [])
        if row[4]:
            feed[post_id][4].append((row[4], row[5], row[6]))

    # Close database connection and return feed
    conn.close()
    return list(feed.values())

def create_post(author_id, title, content):
    """Creates a new post in the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO posts (author_id, title, content, timestamp) VALUES (?,?,?,?)',
                   (author_id, title, content, timestamp))
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return post_id

def delete_post(post_id):
    """Deletes a post from the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE _id =?', (post_id,))
    conn.commit()
    changes = conn.total_changes
    conn.close()
    return not changes

def fetch_post_feed():
    """Fetches all posts from the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    conn.close()
    return posts

