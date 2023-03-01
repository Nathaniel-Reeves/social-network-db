import sqlite3
import bcrypt
import os
import models

def main():
    if os.path.exists(models.DATABASE):
        os.remove(models.DATABASE)
        if __name__ == "__main__":
            print(f"The file {models.DATABASE} has been deleted.")
    else:
        print(f"The file {models.DATABASE} does not exist in the current working directory.")

    conn = sqlite3.connect(models.DATABASE)
    c = conn.cursor()

    # create people table
    c.execute('''CREATE TABLE people (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        username TEXT UNIQUE,
        encrypted_password TEXT
    )''')
    conn.commit()

    # create posts table
    c.execute('''CREATE TABLE posts (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER,
        title TEXT,
        content TEXT,
        timestamp INTEGER,
        FOREIGN KEY(author_id) REFERENCES people(_id) ON DELETE CASCADE
    )''')
    conn.commit()

    # create comments table
    c.execute('''CREATE TABLE comments (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        author_id INTEGER,
        content TEXT,
        timestamp INTEGER,
        FOREIGN KEY(post_id) REFERENCES posts(_id) ON DELETE CASCADE,
        FOREIGN KEY(author_id) REFERENCES people(_id) ON DELETE CASCADE
    )''')
    conn.commit()

    # create following table
    c.execute('''CREATE TABLE following (
        _id INTEGER,
        following_id INTEGER,
        PRIMARY KEY(_id, following_id)
    )''')
    conn.commit()

    # insert 10 rows of random user data
    people = [
        (1, "John Smith", "johnsmith", "p@ssw0rd"),
        (2, "Jane Doe", "janedoe", "qwerty123"),
        (3, "Bob Johnson", "bobjohnson", "letmein"),
        (4, "Emily Davis", "emilydavis", "abc123"),
        (5, "David Lee", "davidlee", "password1"),
        (6, "Samantha Jones", "samanthajones", "changeme"),
        (7, "Michael Brown", "michaelbrown", "123456"),
        (8, "Laura Taylor", "laurataylor", "welcome1"),
        (9, "Chris Wilson", "chriswilson", "secret123"),
        (10, "Amanda Rodriguez", "amandarodriguez", "letmein123")
    ]

    for i in range(len(people)):
        encrypted_password = bcrypt.hashpw(people[i][3].encode('utf-8'), models.SALT)
        c.execute('''INSERT INTO people (
            _id,
            name,
            username,
            encrypted_password
        ) VALUES (?,?,?,?)''', (
            people[i][0],
            people[i][1],
            people[i][2],
            encrypted_password
            )
        )
        conn.commit()

    # insert post data
    posts = [
        (1, 2, "A journey through the mountains",
        "The mountains are beautiful and mesmerizing. There's something about them that draws people in and makes them feel alive. Join me on my journey through the mountains and experience the thrill of adventure!", "2022-02-15 16:02:00"),
        (2, 5, "Exploring the deep blue sea",
        "Dive into the depths of the ocean and discover a world unlike any other. Swim alongside sharks, explore ancient shipwrecks, and come face to face with creatures you've never even heard of. Join me on my journey through the sea!", "2022-02-14 10:30:00"),
        (3, 3, "A day in the life of a farmer",
        "Farming isn't just a job, it's a way of life. From sunrise to sunset, farmers work tirelessly to provide for their families and communities. Join me on my farm and see what it takes to be a successful farmer!", "2022-02-13 18:45:00"),
        (4, 10, "The magic of the Northern Lights",
        "There's nothing quite like seeing the Northern Lights. The way they dance across the sky is truly magical. Join me on a journey to the far north and witness the beauty of the Aurora Borealis!", "2022-02-12 22:15:00"),
        (5, 1, "Baking with grandma",
        "Some of the best memories are made in the kitchen. Join me and my grandma as we bake her famous apple pie. She'll share her secret recipe and we'll enjoy a slice of warm, delicious pie together!", "2022-02-11 08:00:00"),
        (6, 7, "A day in the life of a nurse",
        "Nursing is a tough job, but it's also incredibly rewarding. From taking care of patients to working as part of a team, nurses do it all. Join me on a day in the life of a nurse and see what it takes to care for others.", "2022-02-10 14:20:00"),
        (7, 4, "Hiking the Pacific Crest Trail",
        "The Pacific Crest Trail is one of the most beautiful and challenging hiking trails in the world. Join me on my journey as I hike from Mexico to Canada, covering over 2,600 miles of stunning scenery and rugged terrain.", "2022-02-09 12:00:00"),
        (8, 9, "Solving the world's biggest problems",
        "There are a lot of problems in the world, but there are also a lot of people working to solve them. Join me on my journey as I meet some of the brightest minds in science, technology, and engineering, and learn how they're making a difference in the world.", "2022-02-08 09:30:00")
    ]

    for i in range(len(posts)):
        c.execute('''INSERT INTO posts (
            _id,
            author_id,
            title,
            content,
            timestamp
        ) VALUES (?,?,?,?,?)''', (
            posts[i][0],
            posts[i][1],
            posts[i][2],
            posts[i][3],
            posts[i][4]
            )
        )
        conn.commit()

    # create follower relationships between users
    following = [
        (1, 2),
        (5, 1),
        (2, 3),
        (3, 4),
        (4, 8),
        (5, 7),
        (6, 7),
        (7, 8),
        (8, 9),
        (1, 3),
        (9, 3),
        (4, 5),
        (1, 5),
        (3, 8)
    ]

    for i in range(len(following)):
        c.execute('''INSERT INTO following (
            _id,
            following_id
        ) VALUES (?,?)''', (
            following[i][0],
            following[i][1]
            )
        )
        conn.commit()

    # create comments to posts
    comments = [
        (1, 1, 5, "The mountains are truly breathtaking! I'm glad you had a great time exploring them.",
        "2022-08-01 12:34:56"),
        (2, 1, 3, "I've always wanted to go on a mountain adventure like this. Thanks for sharing your experience!", "2022-08-02 09:21:43"),
        (3, 1, 8, "I agree, there's something about mountains that's just so invigorating. Can't wait to go on my own journey someday!", "2022-08-03 16:57:22"),
        (4, 2, 9, "Wow, the deep sea looks absolutely mesmerizing. I'm so jealous you got to see it in person!", "2022-08-04 10:09:37"),
        (5, 2, 2, "Swimming with sharks? That sounds so cool and terrifying at the same time!",
        "2022-08-05 14:26:18"),
        (6, 2, 4, "I've always been fascinated by the ocean. Your post made me want to book a diving trip ASAP.", "2022-08-06 11:05:42"),
        (7, 3, 1, "It's amazing to see all the hard work that goes into farming. Thanks for sharing your experience!", "2022-08-07 08:14:59"),
        (8, 3, 7, "I have so much respect for farmers. They truly are the backbone of our society.",
        "2022-08-08 20:43:12"),
        (9, 3, 10, "I grew up on a farm myself, and your post brought back a lot of memories. Thanks for the trip down memory lane!", "2022-08-09 15:32:37"),
        (10, 4, 6, "The Northern Lights are one of the most magical things I've ever seen. I'm so glad you got to experience them!", "2022-08-10 09:58:21"),
        (11, 4, 1, "I've always wanted to see the Aurora Borealis. Your post just made me want to go even more.", "2022-08-11 13:45:27"),
        (12, 4, 8, "Wow, the pictures you posted are absolutely stunning. Thanks for sharing them with us!", "2022-08-12 17:22:10"),
        (13, 5, 2, "Baking with grandma is always a treat. I'm so glad you were able to make some memories with her.", "2022-08-13 12:09:32"),
        (14, 5, 3, "Your grandma's apple pie sounds amazing. Would you be willing to share the recipe? ;)",
        "2022-08-14 09:53:57"),
        (15, 5, 7, "I miss baking with my grandma. Your post made me want to give her a call and schedule a baking day ASAP!", "2022-08-15 14:08:21"),
        (16, 6, 10, "Nursing is such an important job. Thanks for sharing your experience with us!",
        "2022-08-16 11:37:44"),
        (17, 6, 4, "I don't think I could ever handle the pressure of being a nurse. Your post made me appreciate them even more.", "2022-08-17 16:45:09"),
        (18, 6, 8, "You nurses are the real heroes! Thanks for all that you do.",
        "2022-08-18 07:39:22"),
        (19, 7, 3, "Hiking the Pacific Crest Trail is definitely on my bucket list. I'm so glad you were able to experience it!", "2022-08-19 14:58:31"),
        (20, 7, 9, "Over 2,600 miles? That's insane! Congratulations on completing such an incredible journey.", "2022-08-20 09:12:14"),
        (21, 7, 2, "I love hiking, but I don't think I could handle such a long and challenging trail. Your post definitely inspired me to push myself more though!", "2022-08-21 18:06:37"),
        (22, 8, 5, "It's amazing to see people working towards making the world a better place. Thanks for sharing their stories with us!", "2022-08-22 11:21:49"),
        (23, 8, 7, "I'm always so impressed by people who are making a real difference in the world. Your post made me want to get involved in my community more.", "2022-08-23 15:30:05"),
        (24, 8, 2, "These scientists and engineers are truly the brightest minds of our generation. Thanks for giving them a platform to share their work!", "2022-08-24 08:47:52")
    ]

    for i in range(len(comments)):
        c.execute('''INSERT INTO comments (
            _id,
            post_id,
            author_id,
            content,
            timestamp
        ) VALUES (?,?,?,?,?)''', (
            comments[i][0],
            comments[i][1],
            comments[i][2],
            comments[i][3],
            comments[i][4]
            )
        )
        conn.commit()

    if __name__ == '__main__':
        print("{} file was successfully created!".format(models.DATABASE))

if __name__ == "__main__":
    main()