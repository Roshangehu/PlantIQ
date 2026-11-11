from backend.database.connection import get_connection
import uuid


def create_chat(title):

    chat_id = str(uuid.uuid4())

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO chats (chat_id, title)
        VALUES (?, ?)
        """,
        (chat_id, title)
    )

    connection.commit()
    connection.close()

    return chat_id


def save_message(chat_id, role, content):

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO messages (chat_id, role, content)
        VALUES (?, ?, ?)
        """,
        (chat_id, role, content)
    )

    connection.execute(
        """
        UPDATE chats
        SET updated_at = CURRENT_TIMESTAMP
        WHERE chat_id = ?
        """,
        (chat_id,)
    )

    connection.commit()
    connection.close()


def get_chat_messages(chat_id):

    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT role, content, timestamp
        FROM messages
        WHERE chat_id = ?
        ORDER BY message_id ASC
        """,
        (chat_id,)
    )

    messages = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return messages


def get_all_chats():

    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT chat_id, title, created_at, updated_at
        FROM chats
        ORDER BY updated_at DESC
        """
    )

    chats = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return chats


def delete_chat(chat_id):

    connection = get_connection()

    connection.execute(
        "DELETE FROM chats WHERE chat_id = ?",
        (chat_id,)
    )

    connection.commit()
    connection.close()