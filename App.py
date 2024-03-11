import tkinter as tk
from typing import List, Callable
from tkinter import messagebox
from Database import Database
from Types import TodoDict

theme = {
    "header": "#002D62",
    "button": "#007FFF",
    "delete": "#E52825",
    "complete": "#148935",
    "is_complete": "#89E0A2",
    "background": "#e4ebf2",
}


class Todo:
    root: tk.Tk
    list_frame: tk.Frame
    todo_id: int
    todo_text: str
    is_complete: bool
    delete_todo: Callable
    toggle_complete_todo: Callable
    todo_frame: tk.Frame
    text_label: tk.Label
    delete_button: tk.Button
    complete_button: tk.Button

    def __init__(
        self,
        root: tk.Tk,
        list_frame: tk.Frame,
        todo_id: int,
        todo_text: str,
        is_complete: bool,
        delete_todo: Callable,
        toggle_complete_todo: Callable
    ):
        self.root = root
        self.list_frame = list_frame
        self.todo_id = todo_id
        self.todo_text = todo_text
        self.is_complete = is_complete
        self.delete_todo = delete_todo
        self.toggle_complete_todo = toggle_complete_todo
        self.create()

    def create(self):
        self.todo_frame = tk.Frame(
            self.list_frame,
            bg="white" if not self.is_complete else theme["is_complete"],
            padx=2,
        )
        self.todo_frame.pack(fill=tk.X, pady=3)

        self.text_label = tk.Label(
            self.todo_frame,
            text=self.todo_text,
            anchor="w",
            justify="left",
            bg="white" if not self.is_complete else theme["is_complete"],
            font=("Segoe UI", 11),
            padx=6,
            pady=6,
            wraplength=400,
        )

        self.delete_button = tk.Button(
            self.todo_frame,
            text="Delete",
            command=self.handle_delete,
            bg=theme["delete"],
            activebackground=theme["delete"],
            fg="white",
            activeforeground="white",
            bd=0,
            font=("Segoe UI", 10),
            padx=6,
            pady=4,
        )

        self.complete_button = tk.Button(
            self.todo_frame,
            text="Mark completed" if not self.is_complete else "Mark not completed",
            command=self.handle_toggle_complete,
            bg=theme["complete"],
            activebackground=theme["complete"],
            fg="white",
            activeforeground="white",
            bd=0,
            font=("Segoe UI", 10),
            padx=6,
            pady=4,
        )

        self.text_label.pack(fill=tk.X)
        self.complete_button.pack(side=tk.RIGHT, padx=2, pady=4)
        self.delete_button.pack(side=tk.RIGHT, padx=2, pady=4)

    def handle_delete(self):
        self.delete_todo(self.todo_id)

    def handle_toggle_complete(self):
        self.toggle_complete_todo(self.todo_id)

    def destroy(self):
        self.todo_frame.destroy()


class TodoInput:
    root: tk.Tk
    input_frame: tk.Frame
    add_todo: Callable
    input_box: tk.Entry
    submit_button: tk.Button

    def __init__(self, root: tk.Tk, input_frame: tk.Frame, add_todo: Callable):
        self.root = root
        self.input_frame = input_frame
        self.add_todo = add_todo
        self.create()

    def create(self):
        self.input_box = tk.Entry(
            font=("Segoe UI", 12),
            highlightbackground="white",
            highlightcolor="white",
            highlightthickness=10,
            bd=0,
            relief="flat",
        )

        self.submit_button = tk.Button(
            text="Add todo",
            command=self.handle_submit,
            padx=10,
            pady=10,
            bd=0,
            font=("Segoe UI Bold", 12),
            bg=theme["button"],
            activebackground=theme["button"],
            fg="#fff",
            activeforeground="#fff",
        )

        self.input_box.pack(fill=tk.X)
        self.input_box.focus_set()
        self.submit_button.pack(fill=tk.X)

    def handle_submit(self):
        if len(self.input_box.get()) == 0:
            messagebox.showwarning(
                "Empty todo",
                "You cannot add a todo with no text!\nEnter at least 1 character before adding your todo."
            )
            return

        self.add_todo(self.input_box.get())
        self.input_box.delete(0, tk.END)


class TodoApp:
    root: tk.Tk
    header_frame: tk.Frame
    header_label: tk.Label
    list_frame: tk.Frame
    input_frame: tk.Frame
    todo_input: TodoInput
    todos: List[TodoDict]
    todo_objects: List[Todo]
    database: Database

    def __init__(self):
        self.root = tk.Tk()
        self.todos = []
        self.todo_objects = []
        self.database = Database()
        self.create_layout()
        self.display_todos()

    def create_layout(self):
        self.root.geometry("400x700")
        self.root.resizable(width=False, height=True)
        self.root.title("Todo App!")

        self.header_frame = tk.Frame(self.root)
        self.list_frame: tk.Frame = tk.Frame(self.root, bg=theme["background"], pady=3)
        self.input_frame: tk.Frame = tk.Frame(self.root, bg="white")

        self.header_frame.pack(fill=tk.X)
        self.list_frame.pack(fill=tk.BOTH, expand=True)
        self.input_frame.pack(fill=tk.X)

        self.header_label = tk.Label(
            self.header_frame,
            text="Todo App!",
            bg=theme["header"],
            fg="#fff",
            font=("Segoe UI Bold", 12),
            pady=14,
        )
        self.header_label.pack(fill=tk.X)

        # input
        self.todo_input = TodoInput(self.root, self.input_frame, self.add_todo)

    def display_todos(self):
        for obj in self.todo_objects:
            obj.destroy()

        self.todo_objects.clear()

        # Populate todos from db
        self.todos = self.database.get_todos()

        for i in range(len(self.todos)):
            self.todo_objects.append(
                Todo(
                    self.root,
                    self.list_frame,
                    self.todos[i]['todo_id'],
                    self.todos[i]['todo_text'],
                    self.todos[i]['is_complete'],
                    self.delete_todo,
                    self.toggle_complete_todo,
                )
            )

    def add_todo(self, todo_text: str):
        self.database.add_todo(todo_text)
        self.display_todos()

    def delete_todo(self, todo_id: int):
        self.database.delete_todo(todo_id)
        self.display_todos()

    def toggle_complete_todo(self, todo_id: int):
        target_todo = None

        for todo in self.todos:
            if todo['todo_id'] == todo_id:
                target_todo = todo
                break

        current_status = target_todo['is_complete']
        is_complete_status_to_set = 1 if not current_status else 0
        self.database.set_todo_complete_status(todo_id, is_complete_status_to_set)
        self.display_todos()

    def run(self):
        self.root.mainloop()


def main():
    todo_app = TodoApp()
    todo_app.run()
    pass


if __name__ == "__main__":
    main()
