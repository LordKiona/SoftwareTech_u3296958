import tkinter as tk
from tkinter import messagebox
import time
import random
import string
from collections import deque

class Node:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None


class ContactDirectory:
    def __init__(self):
        self.root = None

    def insert(self, root, name, phone):
        if root is None:
            return Node(name, phone)

        if name < root.name:
            root.left = self.insert(root.left, name, phone)
        elif name > root.name:
            root.right = self.insert(root.right, name, phone)
        else:
            root.phone = phone  # update existing

        return root

    def search(self, root, name):
        if root is None or root.name == name:
            return root

        if name < root.name:
            return self.search(root.left, name)
        else:
            return self.search(root.right, name)

    def find_min(self, root):
        while root.left:
            root = root.left
        return root

    def delete(self, root, name):
        if root is None:
            return root

        if name < root.name:
            root.left = self.delete(root.left, name)
        elif name > root.name:
            root.right = self.delete(root.right, name)
        else:
            # 0 or 1 child
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            # 2 children
            temp = self.find_min(root.right)
            root.name = temp.name
            root.phone = temp.phone
            root.right = self.delete(root.right, temp.name)

        return root

    def inorder(self, root, result=None):
        if result is None:
            result = []

        if root:
            self.inorder(root.left, result)
            result.append((root.name, root.phone))
            self.inorder(root.right, result)

        return result

class BSTApp:
    def __init__(self, root):
        self.directory = ContactDirectory()
        self.root = root
        self.root.title("BST Contact Directory")

        # Inputs
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(frame, text="Phone").grid(row=1, column=0)
        self.phone_entry = tk.Entry(frame)
        self.phone_entry.grid(row=1, column=1)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Insert", command=self.insert).grid(row=0, column=0)
        tk.Button(btn_frame, text="Search", command=self.search).grid(row=0, column=1)
        tk.Button(btn_frame, text="Delete", command=self.delete).grid(row=0, column=2)
        tk.Button(btn_frame, text="Show All", command=self.show_all).grid(row=0, column=3)
        tk.Button(btn_frame, text="Benchmark", command=self.benchmark).grid(row=0, column=4)

        # Output box
        self.output = tk.Text(root, height=10, width=60)
        self.output.pack(pady=10)

    def insert(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("Error", "Enter name & phone")
            return

        self.directory.root = self.directory.insert(self.directory.root, name, phone)
        messagebox.showinfo("Success", f"{name} added/updated")
        self.clear()
        self.show_all()

    def search(self):
        name = self.name_entry.get().strip()
        node = self.directory.search(self.directory.root, name)

        self.output.delete(1.0, tk.END)

        if node:
            self.output.insert(tk.END, f"Found:\n{name} - {node.phone}")
        else:
            self.output.insert(tk.END, "Not found")

    def delete(self):
        name = self.name_entry.get().strip()

        self.directory.root = self.directory.delete(self.directory.root, name)
        messagebox.showinfo("Deleted", f"{name} removed (if existed)")
        self.clear()
        self.show_all()

    def show_all(self):
        self.output.delete(1.0, tk.END)
        contacts = self.directory.inorder(self.directory.root)

        if not contacts:
            self.output.insert(tk.END, "No contacts")
        else:
            for name, phone in contacts:
                self.output.insert(tk.END, f"{name} - {phone}\n")

    def clear(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)


    def benchmark(self):
        self.directory.root = None

        N = 100000
        names = [''.join(random.choices(string.ascii_lowercase, k=6)) for _ in range(N)]
        phones = [''.join(random.choices(string.digits, k=10)) for _ in range(N)]

        # Insert
        start = time.time()
        for i in range(N):
            self.directory.root = self.directory.insert(self.directory.root, names[i], phones[i])
        insert_time = time.time() - start

        # Search
        start = time.time()
        for name in names[:500]:
            self.directory.search(self.directory.root, name)
        search_time = time.time() - start

        # Delete
        start = time.time()
        for name in names[:100]:
            self.directory.root = self.directory.delete(self.directory.root, name)
        delete_time = time.time() - start

        # Show results
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END,
            f"Benchmark (N=1000)\n"
            f"Insert: {insert_time:.4f}s\n"
            f"Search: {search_time:.4f}s\n"
            f"Delete: {delete_time:.4f}s\n"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = BSTApp(root)
    root.mainloop()