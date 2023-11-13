import os
import sqlite3


def connect(path: str | None = None):
    if path is None:
        path = os.environ.get("DB_PATH", "sqlite3.db")

    con = sqlite3.connect(path, check_same_thread=False)
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.executescript(
        """
    CREATE TABLE IF NOT EXISTS "USERS"(
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "email" TEXT NOT NULL,
        "username" TEXT,
        "hashed_password" TEXT NOT NULL,
        "state_comment" TEXT
    );

    CREATE TABLE IF NOT EXISTS "FOLLOW_REQUEST"(
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "username" TEXT NOT NULL,
        "target_username" TEXT NOT NULL,
        "following_state" INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "MATE_RELATIONSHIP"(
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "first_username" TEXT NOT NULL,
        "second_username" TEXT NOT NULL 
    );
    """
    )

    cur.close()

    return con


# add_user in database
def add_user(
    user_id: int,
    email: str,
    hash: str,
    username: str | None = None,
    state_comment: str | None = None,
):
    """Add user to database

    CREATE TABLE IF NOT EXISTS "USERS"(
         "id" INTEGER PRIMARY KEY AUTOINCREMENT,
         "email" TEXT NOT NULL,
         "username" TEXT,
         "hashed_password" TEXT NOT NULL,
         "state_comment" TEXT
     );

    Arguments:
     user_id (int): id
     email (str): email
     hash (str): hashed_password
     state_comment (str): state_comment
    """
    con = connect()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO Users(id,email,username,hashed_password,state_comment) VALUES(?,?,?,?,?)",
        (user_id, email, username, hash, state_comment),
    )
    con.commit()


def get_user(email: str):
    """Get user from database

    CREATE TABLE IF NOT EXISTS "USERS"(
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "email" TEXT NOT NULL,
        "username" TEXT,
        "hashed_password" TEXT NOT NULL,
        "state_comment" TEXT
    );

    Arguments:
        user_id (int): id
        email (str): email
        hash (str): hashed_password
        state_comment (str): state_comment
    """
    con = connect()
    cur = con.cursor()

    cur.execute("SELECT * FROM USERS WHERE email=?", (email,))
    user = cur.fetchone()
    return user
    ...

