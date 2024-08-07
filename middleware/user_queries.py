from werkzeug.security import generate_password_hash
from psycopg2.extensions import cursor as PgCursor
from typing import Dict


def user_check_email(cursor: PgCursor, email: str) -> Dict[str, str]:
    """
    Checks if a user with the given email exists in the database.

    :param cursor: A psycopg2 cursor object to execute database queries.
    :param email: The email address to check against the users in the database.
    :return: A dictionary with the user's ID if found, otherwise an error message.
    """
    cursor.execute("select id from users where email = ?", (email, ))
    results = cursor.fetchall()
    if len(results) > 0:
        user_data = {"id": results[0][0]}
        return user_data
    else:
        return {"error": "no match"}


def user_post_results(cursor: PgCursor, email: str, password: str) -> None:
    """
    Creates a new user with the provided email and password.

    :param cursor: A psycopg2 cursor object to execute database queries.
    :param email: The email address of the new user.
    :param password: The password for the new user.
    """
    password_digest = generate_password_hash(password)
    cursor.execute(
        "insert into users (email, password_digest) values (?, ?)", 
    (email, password_digest, ))

    return
