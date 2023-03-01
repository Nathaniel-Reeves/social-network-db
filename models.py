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
        WHERE people.username = ? ''', (username,))
    result = cursor.fetchone()
    conn.close()
    return not not result

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
    cursor.execute('SELECT _id, author_id, title, content FROM posts')
    posts = cursor.fetchall()
    conn.close()
    return posts

def get_most_active_user():
    """Returns the user with the most posts and comments on other posts."""

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get all users with their posts and comments count
    cursor.execute('''
        SELECT people.username, COUNT(DISTINCT posts._id) AS num_posts,
        COUNT(DISTINCT comments._id) AS num_comments
        FROM people
        LEFT JOIN posts ON people._id = posts.author_id
        LEFT JOIN comments ON people._id = comments.author_id
        GROUP BY people.username
    ''')
    users = cursor.fetchall()

    # Find the user with the highest sum of posts and comments count
    most_active_user = None
    max_posts_comments = 0
    for user in users:
        posts_comments = user[1] + user[2]
        if posts_comments > max_posts_comments:
            max_posts_comments = posts_comments
            most_active_user = user[0]

    # Close database connection and return most active user
    conn.close()
    return most_active_user


def add_follower(user_id, follower_id):
    """Adds a follower to a user in the database.
    Args:
        user_id (int): The ID of the user being followed.
        follower_id (int): The ID of the follower.
    Returns:
        str: Message indicating whether the follower was added.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if user with given ID exists
    cursor.execute('SELECT * FROM people WHERE _id = ?', (user_id,))
    user = cursor.fetchone()
    if not user:
        return "User not found"

    # Check if follower with given ID exists
    cursor.execute('SELECT * FROM people WHERE _id = ?', (follower_id,))
    follower = cursor.fetchone()
    if not follower:
        return "Follower not found"

    # Check if follower is already following user
    cursor.execute('SELECT * FROM following WHERE _id = ? AND following_id = ?',
                   (user_id, follower_id))
    existing_follower = cursor.fetchone()
    if existing_follower:
        return "Follower already exists"

    # Insert new follower into followers table
    cursor.execute('INSERT INTO following (_id, following_id) VALUES (?, ?)',
                   (user_id, follower_id))
    conn.commit()

    # Close database connection and return success message
    conn.close()
    return "Follower added"


def remove_follower(follower_id, followed_id):
    """Removes a follower from a user's list of followers.
    Args:
        follower_id (int): The ID of the user who is following.
        followed_id (int): The ID of the user being followed.
    Returns:
        str: Message indicating whether follower was removed or not.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if follower exists
    cursor.execute('SELECT * FROM people WHERE _id = ?', (follower_id,))
    follower = cursor.fetchone()
    if not follower:
        conn.close()
        return f"User with ID {follower_id} does not exist."

    # Check if followed user exists
    cursor.execute('SELECT * FROM people WHERE _id = ?', (followed_id,))
    followed = cursor.fetchone()
    if not followed:
        conn.close()
        return f"User with ID {followed_id} does not exist."

    # Check if follower is already following followed user
    cursor.execute('SELECT * FROM following WHERE _id = ? AND following_id = ?',
                   (follower_id, followed_id))
    existing_follower = cursor.fetchone()
    if not existing_follower:
        conn.close()
        return f"User with ID {follower_id} is not following user with ID {followed_id}."

    # Remove follower from database
    cursor.execute('DELETE FROM following WHERE _id = ? AND following_id = ?',
                   (follower_id, followed_id))
    conn.commit()
    conn.close()

    return f"User with ID {follower_id} successfully unfollowed user with ID {followed_id}."


def get_followers_and_following(user_id):
    """Get list of followers and users being followed by user with given ID.
    Args:
        user_id (int): The ID of the user.
    Returns:
        Tuple[List[str], List[str]]: The first list contains the usernames of followers, the second list contains the usernames of users being followed.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get list of followers
    cursor.execute(
        'SELECT people.username FROM people INNER JOIN following ON people._id = following._id WHERE following.following_id = ?', (user_id,))
    followers = [row[0] for row in cursor.fetchall()]

    # Get list of users being followed
    cursor.execute(
        'SELECT people.username FROM people INNER JOIN following ON people._id = following.following_id WHERE following._id = ?', (user_id,))
    following = [row[0] for row in cursor.fetchall()]

    # Close database connection and return results
    conn.close()
    return followers, following


def get_bacon_number(lookup_user_id):
    """Returns the bacon number of other users to a lookup user.
    bacon number is calculated by the number of followers awway from
    the lookup user."""

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    people_table_size = cursor.execute(
        "SELECT COUNT(*) FROM people").fetchone()[0] - 1

    cursor.execute('''
    SELECT
        _id,
        name,
        MIN(bacon_number) as n
    FROM(
        SELECT
        *
        FROM(
            WITH RECURSIVE bacon_numbers(_id, name, bacon_number) AS(
                SELECT
                    _id,
                    name,
                    0 AS bacon_number
                FROM people
                WHERE _id= {lookup_user_id}

                UNION

                SELECT
                    p._id,
                    p.name,
                    bn.bacon_number + 1
                FROM following f1
                JOIN bacon_numbers bn ON
                    bn._id=f1._id
                JOIN people p ON
                    f1.following_id=p._id
                WHERE bn.bacon_number < {table_size}
            )
            SELECT
            *
            FROM bacon_numbers
        )

        UNION

        SELECT
        *
        FROM(
            WITH RECURSIVE bacon_numbers(_id, name, bacon_number) AS(
                SELECT
                    _id,
                    name,
                    0 AS bacon_number
                FROM people
                WHERE _id= {lookup_user_id}

                UNION

                SELECT
                    p._id,
                    p.name,
                    bn.bacon_number + 1
                FROM following f1
                JOIN bacon_numbers bn ON
                    bn._id=f1.following_id
                JOIN people p ON
                    f1._id=p._id
                WHERE bn.bacon_number < {table_size}
            )
            SELECT
            *
            FROM bacon_numbers
        )
    )
    GROUP BY
        _id
    ORDER BY
        bacon_number,
        name DESC
    '''.format(lookup_user_id=lookup_user_id, table_size=people_table_size))

    bacon_numbers = cursor.fetchall()

    # Close database connection and return bacon number
    conn.close()
    return bacon_numbers
