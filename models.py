import sqlite3
import bcrypt

DATABASE = 'test.db'
SALT = b'$2b$12$bCkhk/dnjeaHnxqYLh39be'

def valid_user(username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        SELECT
            people.username,
            people.encrypted_password
        FROM people 
        WHERE people.username = ? ''', (username,))
    result = c.fetchone()
    conn.close()
    check = bcrypt.checkpw(password.encode("utf-8"), result[1])
    return check
