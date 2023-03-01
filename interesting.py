"""
Notes from the assignment: 
    You must also implement at least two "interesting" queries on that database you have created. These should do something challenging beyond the basic "select .. from .. join .. where .. group by .. having .. order by" form. Be creative! Show off!
"""
import sqlite3
import models
"""
Interesting query #1: Recursive "bacon number" interactions from
one user to another user through followers and followies.

Query Author: Nathaniel Reeves
"""


def get_bacon_number(lookup_user_id):
    """Returns the bacon number of other users to a lookup user.
    bacon number is calculated by the number of followers awway from
    the lookup user."""

    conn = sqlite3.connect(models.DATABASE)
    cursor = conn.cursor()

    people_table_size = cursor.execute("SELECT COUNT(*) FROM people").fetchone()[0] - 1


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

"""
Interesting query #2: Most active user, i.e. the user with the 
most posts and comments on other posts.
Query Author: Marie Elsewell
"""


def get_most_active_user():
    """Returns the user with the most posts and comments on other posts."""

    conn = sqlite3.connect(models.DATABASE)
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
