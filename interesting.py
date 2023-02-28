"""
Notes from the assignment: 
    You must also implement at least two "interesting" queries on that database you have created. These should do something challenging beyond the basic "select .. from .. join .. where .. group by .. having .. order by" form. Be creative! Show off!
"""
import sqlite3
import models
"""
Interesting query #1: Recursive "bacon number" interactions
one user to another user through friends and comments.
Query Author: Nathaniel Reeves
"""

"""
Interesting query #2: Most active user, i.e. the user with the 
most posts and comments on other posts.
Query Author: Marie Elsewell
"""


def get_most_active_user():
    conn = sqlite3.connect(models.DATABASE)
    cursor = conn.cursor()

    # Get all users
    cursor.execute('SELECT _id, username FROM people')
    users = cursor.fetchall()

    # Initialize dictionary to keep track of activity counts
    activity_counts = {}
    for user in users:
        activity_counts[user[0]] = 0

    # Get counts of posts for each user
    cursor.execute('SELECT author_id, COUNT(*) FROM posts GROUP BY author_id')
    post_counts = cursor.fetchall()
    for post_count in post_counts:
        activity_counts[post_count[0]] += post_count[1]

    # Get counts of comments for each user
    cursor.execute(
        'SELECT author_id, COUNT(*) FROM comments GROUP BY author_id')
    comment_counts = cursor.fetchall()
    for comment_count in comment_counts:
        activity_counts[comment_count[0]] += comment_count[1]

    # Get user with highest activity count
    most_active_user_id = max(activity_counts, key=activity_counts.get)

    # Get username of most active user
    cursor.execute('SELECT username FROM people WHERE _id = ?',
                   (most_active_user_id,))
    most_active_user = cursor.fetchone()[0]

    # Close database connection and return most active user
    conn.close()
    return most_active_user
