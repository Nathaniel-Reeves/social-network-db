# social-network-db
This is for a social network assignment for CS4307.  A simple implementation of a sqlite database with a python interface.

## main.py file
main.py is the main module of the social media platform, responsible for running the application and handling user input. It uses the Flask framework to create a web server that listens for requests from clients, such as web browsers, and responds to those requests with HTML, CSS, and JavaScript. The code defines routes that correspond to different URLs that the application can handle, such as viewing a user's profile or creating a new post.

The main.py file also interacts with the models.py module, which provides functions for interacting with the SQLite database that stores user information and posts. For example, the create_post function in models.py is called when a user creates a new post through the web interface.

## models.py file
The models.py module defines functions for interacting with the SQLite database that stores user information and posts. The module uses the sqlite3 library to connect to the database, and also includes functions for hashing passwords and validating user credentials.

Functions in models.py include valid_user, which checks if a user with the given username and password exists in the database, create_user, which creates a new user in the database, and create_post, which creates a new post in the database. The module also includes functions for getting information about users and their posts, such as get_users and get_posts_by_user_id.

The models.py file is called by the main.py module, which uses these functions to interact with the database and generate HTML pages in response to user requests.

## init_db.py file

To initilaize the database using the the init_db.py file, follow these steps:

1.Open a command prompt or terminal and navigate to the directory containing the init_db.py file.
2.Run the command "python init_db.py" to execute the Python script.
3.The script will create a new SQLite database file named "blog.db" in the same directory as the init_db.py file.
4.The script will also create four tables named "people", "posts", "comments", and "following", and insert sample data into the "people" and "posts" tables.
5.If the "blog.db" file already exists in the directory, the script will delete it and create a new one.

Note: Make sure that you have the necessary dependencies installed (such as SQLite and bcrypt) before running the script. Also, be careful when executing scripts from unknown sources, as they may contain malicious code.

## data structure

The application's database schema consists of four tables: people, posts, comments, and following. Here are the create table statements for each table:

### People Table

``` sql
CREATE TABLE people (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT UNIQUE,
    encrypted_password TEXT
)

```
### Posts Table
``` sql
CREATE TABLE posts (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER,
    title TEXT,
    content TEXT,
    timestamp INTEGER,
    FOREIGN KEY(author_id) REFERENCES people(_id) ON DELETE CASCADE
)
```
### Comments Table
``` sql
CREATE TABLE comments (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    author_id INTEGER,
    content TEXT,
    timestamp INTEGER,
    FOREIGN KEY(post_id) REFERENCES posts(_id) ON DELETE CASCADE,
    FOREIGN KEY(author_id) REFERENCES people(_id) ON DELETE CASCADE
)
```
### Following Table
``` sql
CREATE TABLE following (
    _id INTEGER,
    following_id INTEGER,
    PRIMARY KEY(_id, following_id)
)
```
The people table holds user data such as name, username, and encrypted password. The posts table holds data about the blog posts such as the author's ID, title, content, and timestamp. The comments table holds comments on blog posts, and the following table keeps track of users following other users.

Note that the tables are linked using foreign keys and cascading deletes, which helps maintain data integrity.

## Unit Testing this project

Great, here are the commands you can use to run the unittest_projecty.py file:

To run all the tests in the file:
``` bash
python unittest_projecty.py
```
To run specific tests using the test name:
``` bash
python unittest_projecty.py -k test_method_name
```
Replace test_method_name with the actual name of the test method you want to run.

To run specific test classes using the class name:
``` bash
python unittest_projecty.py -k ClassName
```
Replace ClassName with the actual name of the test class you want to run.

To run the tests with more detailed output:
``` bash
python unittest_projecty.py -v
```
The -v flag stands for verbose and will output more information about the tests.

Note that the above commands assume that you have Python installed on your machine and that the unittest_projecty.py file is in the current working directory.