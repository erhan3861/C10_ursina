import tkinter as tk
from tkinter import messagebox

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "admin" and password == "password":
        messagebox.showinfo("Login ok", "Welcome, " + username)
    else:
        messagebox.showerror("Login failed", "username or password wrong")

root = tk.Tk()
root.title("Oyun Giriş Sayfası")
root.geometry("300x200")

label_username = tk.Label(root, text="Kullanıcı Adı:")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Şifre etiketi ve girişi
label_password = tk.Label(root, text="Şifre:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Giriş butonu
button_login = tk.Button(root, text="Giriş Yap", command=login)
button_login.pack(pady=20)

# Ana döngüyü başlatma
root.mainloop()
