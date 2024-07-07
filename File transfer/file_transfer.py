import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
from cryptography.fernet import Fernet
import threading

class AuthSystem:
    def __init__(self):
        self.users = {"user1": "password1", "user2": "password2"}
    
    def authenticate(self, username, password):
        return self.users.get(username) == password

class Encryption:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, data):
        return self.cipher_suite.encrypt(data)

    def decrypt(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data)

class FileManager:
    def __init__(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def list_files(self):
        return os.listdir(self.directory)
    
    def delete_file(self, filename):
        os.remove(os.path.join(self.directory, filename))

class FileSharingApp:
    def __init__(self, root, auth, encryption, file_manager):
        self.root = root
        self.auth = auth
        self.encryption = encryption
        self.file_manager = file_manager

        self.root.title("File Sharing App")

        self.username = None
        
        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.download_button = tk.Button(root, text="Download File", command=self.download_file)
        self.download_button.pack(pady=10)

        self.manage_button = tk.Button(root, text="Manage Files", command=self.manage_files)
        self.manage_button.pack(pady=10)

        self.logout_button = tk.Button(root, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

        self.login()

    def login(self):
        username = simpledialog.askstring("Login", "Enter username:")
        password = simpledialog.askstring("Login", "Enter password:", show='*')

        if self.auth.authenticate(username, password):
            self.username = username
            messagebox.showinfo("Info", "Login successful")
        else:
            messagebox.showerror("Error", "Authentication failed")
            self.root.destroy()

    def logout(self):
        self.username = None
        self.root.quit()
        self.root.update()
        self.root.destroy()
        
    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as f:
                data = f.read()
            encrypted_data = self.encryption.encrypt(data)
            with open(os.path.join(self.file_manager.directory, os.path.basename(file_path)), 'wb') as f:
                f.write(encrypted_data)
            messagebox.showinfo("Info", f"File {file_path} uploaded successfully.")
        
    def download_file(self):
        file_name = simpledialog.askstring("Download", "Enter the file name to download:")
        if file_name:
            file_path = os.path.join(self.file_manager.directory, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()
                data = self.encryption.decrypt(encrypted_data)
                download_path = filedialog.asksaveasfilename(defaultextension=".*", initialfile=file_name)
                with open(download_path, 'wb') as f:
                    f.write(data)
                messagebox.showinfo("Info", f"File {file_name} downloaded successfully.")
            else:
                messagebox.showerror("Error", f"File {file_name} not found.")
        
    def manage_files(self):
        def delete_file():
            file_name = simpledialog.askstring("Delete", "Enter the file name to delete:")
            if file_name:
                file_path = os.path.join(self.file_manager.directory, file_name)
                if os.path.exists(file_path):
                    self.file_manager.delete_file(file_name)
                    messagebox.showinfo("Info", f"File {file_name} deleted successfully.")
                else:
                    messagebox.showerror("Error", f"File {file_name} not found.")

        files = self.file_manager.list_files()
        file_list = "\n".join(files)
        messagebox.showinfo("Files", f"Uploaded files:\n{file_list}")
        
        delete_button = tk.Button(self.root, text="Delete File", command=delete_file)
        delete_button.pack(pady=10)
        
        self.root.mainloop()

def run_app():
    root = tk.Tk()
    auth = AuthSystem()
    encryption = Encryption()
    file_manager = FileManager("./files")  # You can change the path as needed

    app = FileSharingApp(root, auth, encryption, file_manager)
    root.mainloop()

if __name__ == "__main__":
    run_app()
