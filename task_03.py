import tkinter as tk
from tkinter import messagebox, simpledialog

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, prompt=None):
        self.prompt = prompt
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text=self.prompt, font=("Helvetica", 12)).pack(pady=10)
        self.entry = tk.Entry(master, font=("Helvetica", 12), width=30)
        self.entry.pack(pady=10)
        return self.entry

    def apply(self):
        self.result = self.entry.get()

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.contacts = {}
        
        self.load_contacts()
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(
            self.root, 
            text="Contact Management System", 
            font=("Helvetica", 18, "bold"), 
            fg="white", 
            bg="#4A90E2"
        )
        self.title_label.pack(pady=10, fill=tk.X)

        self.contact_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.contact_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.contact_listbox = tk.Listbox(
            self.contact_frame, 
            font=("Helvetica", 12), 
            bg="#FFFFFF", 
            fg="#333333", 
            selectbackground="#4A90E2", 
            selectforeground="#FFFFFF"
        )
        self.contact_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.contact_listbox.bind('<Double-1>', self.view_contact)

        self.button_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(
            self.button_frame, 
            text="Add Contact", 
            font=("Helvetica", 12), 
            bg="#4CAF50", 
            fg="white", 
            command=self.add_contact
        )
        self.add_button.grid(row=0, column=0, padx=10)

        self.view_button = tk.Button(
            self.button_frame, 
            text="View Contact", 
            font=("Helvetica", 12), 
            bg="#2196F3", 
            fg="white", 
            command=self.view_contact_button
        )
        self.view_button.grid(row=0, column=1, padx=5)

        self.edit_button = tk.Button(
            self.button_frame, 
            text="Edit Contact", 
            font=("Helvetica", 12), 
            bg="#FFC107", 
            fg="white", 
            command=self.edit_contact
        )
        self.edit_button.grid(row=0, column=2, padx=5)

        self.remove_button = tk.Button(
            self.button_frame, 
            text="Remove Contact", 
            font=("Helvetica", 12), 
            bg="#F44336", 
            fg="white", 
            command=self.remove_contact
        )
        self.remove_button.grid(row=0, column=3, padx=5)

        self.save_button = tk.Button(
            self.button_frame, 
            text="Save Contacts", 
            font=("Helvetica", 12), 
            bg="#2196F3", 
            fg="white", 
            command=self.save_contacts
        )
        self.save_button.grid(row=0, column=4, padx=5)

        self.update_contact_listbox()

    def add_contact(self):
        name = self.custom_dialog("Input", "Enter name:")
        if name:
            phone = self.custom_dialog("Input", "Enter phone number:")
            email = self.custom_dialog("Input", "Enter email address:")
            self.contacts[name] = {"phone": phone, "email": email}
            self.update_contact_listbox()

    def edit_contact(self):
        try:
            selected_contact = self.contact_listbox.get(self.contact_listbox.curselection())
            if selected_contact:
                phone = self.custom_dialog("Input", "Enter new phone number:", initialvalue=self.contacts[selected_contact]['phone'])
                email = self.custom_dialog("Input", "Enter new email address:", initialvalue=self.contacts[selected_contact]['email'])
                self.contacts[selected_contact] = {"phone": phone, "email": email}
                self.update_contact_listbox()
        except tk.TclError:
            messagebox.showerror("Error", "Please select a contact to edit.")

    def remove_contact(self):
        try:
            selected_contact = self.contact_listbox.get(self.contact_listbox.curselection())
            if selected_contact:
                del self.contacts[selected_contact]
                self.update_contact_listbox()
        except tk.TclError:
            messagebox.showerror("Error", "Please select a contact to remove.")

    def view_contact(self, event):
        self.show_contact_details()

    def view_contact_button(self):
        self.show_contact_details()

    def show_contact_details(self):
        try:
            selected_contact = self.contact_listbox.get(self.contact_listbox.curselection())
            if selected_contact:
                contact_info = self.contacts[selected_contact]
                contact_details = f"Name: {selected_contact}\nPhone: {contact_info['phone']}\nEmail: {contact_info['email']}"

                details_window = tk.Toplevel(self.root)
                details_window.title("Contact Details")
                details_window.geometry("400x200")  

                details_label = tk.Label(details_window, text=contact_details, font=("Helvetica", 14), justify="left")
                details_label.pack(pady=20, padx=20)

                close_button = tk.Button(details_window, text="Close", command=details_window.destroy, font=("Helvetica", 12), bg="#F44336", fg="white")
                close_button.pack(pady=10)
        except tk.TclError:
            messagebox.showerror("Error", "Please select a contact to view.")

    def load_contacts(self):
        try:
            with open("contacts.txt", "r") as file:
                for line in file:
                    name, phone, email = line.strip().split(',')
                    self.contacts[name] = {"phone": phone, "email": email}
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open("contacts.txt", "w") as file:
            for name, info in self.contacts.items():
                file.write(f"{name},{info['phone']},{info['email']}\n")
        messagebox.showinfo("Save Contacts", "Contacts saved successfully!")

    def update_contact_listbox(self):
        self.contact_listbox.delete(0, tk.END)
        for name in self.contacts:
            self.contact_listbox.insert(tk.END, name)

    def custom_dialog(self, title, prompt, initialvalue=""):
        dialog = CustomDialog(self.root, title=title, prompt=prompt)
        return dialog.result

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.geometry("670x400")
    root.mainloop()
