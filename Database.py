import sqlite3
from sqlite3 import Connection, Cursor
from Types import TodoDict
from typing import List


class Database:
    connection: Connection
    cursor: Cursor

    def __init__(self):
        self.create_table()

    def open_connection(self):
        self.connection = sqlite3.connect("todos.db")

    def close_connection(self):
        self.connection.close()

    def create_table(self):
        self.open_connection()
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Todos (
                TodoID INTEGER PRIMARY KEY,
                TodoText TEXT,
                IsComplete INTEGER
            )
        """)

        self.cursor.close()
        self.close_connection()

    def add_todo(self, todo_text: str):
        self.open_connection()
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            INSERT INTO Todos (TodoText, IsComplete)
            VALUES (?, 0)
        """, (todo_text,))
        self.connection.commit()

        self.cursor.close()
        self.close_connection()

    def set_todo_complete_status(self, todo_id: int, is_complete: int):
        self.open_connection()
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            UPDATE Todos
            SET IsComplete = ?
            WHERE TodoID = ?
        """, (is_complete, todo_id,))
        self.connection.commit()

        self.cursor.close()
        self.close_connection()

    def delete_todo(self, todo_id: int):
        self.open_connection()
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            DELETE FROM Todos
            WHERE TodoID = ?
        """, (todo_id,))
        self.connection.commit()

        self.cursor.close()
        self.close_connection()

    def get_todos(self) -> List[TodoDict]:
        self.open_connection()
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            SELECT * FROM Todos
        """)
        results = self.cursor.fetchall()

        self.cursor.close()
        self.close_connection()

        # format todos in expected format
        todos = []
        for result in results:
            todos.append({
                "todo_id": result[0],
                "todo_text": result[1],
                "is_complete": False if result[2] == 0 else True,
            })

        return todos


