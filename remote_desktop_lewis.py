import tkinter as tk
from tkinter import messagebox
import socket
import pyautogui
import threading
import time
from PIL import ImageGrab, ImageTk
import cv2
import numpy as np

admin_user = "reaper"
admin_pass = "nmap:SC.P9"
member_user = "leo"
member_pass = "port80"
visitor_code = "6770"
failed_attempts = 0
max_attempts = 10
admin_ip = socket.gethostbyname(socket.gethostname())

def login_window(user_type, root):
    global failed_attempts

    def check_login():
        global failed_attempts

        if user_type == "admin":
            username = entry_user.get()
            password = entry_pass.get()

            if username == admin_user and password == admin_pass:
                messagebox.showinfo("Login Successful", "Welcome Admin!")
                display_admin_window(root)
            else:
                failed_attempts += 1
                if failed_attempts >= max_attempts:
                    messagebox.showerror("Login Failed", "Too many failed attempts. Closing the application.")
                    root.quit()
                else:
                    messagebox.showerror("Login Failed", f"Invalid credentials. {max_attempts - failed_attempts} attempts left.")
        elif user_type == "member":
            username = entry_user.get()
            password = entry_pass.get()

            if username == member_user and password == member_pass:
                messagebox.showinfo("Login Successful", "Welcome Member!")
                display_member_window(root)
            else:
                failed_attempts += 1
                if failed_attempts >= max_attempts:
                    messagebox.showerror("Login Failed", "Too many failed attempts. Closing the application.")
                    root.quit()
                else:
                    messagebox.showerror("Login Failed", f"Invalid credentials. {max_attempts - failed_attempts} attempts left.")
        elif user_type == "visitor":
            code = entry_code.get()
            if code == visitor_code:
                messagebox.showinfo("Visitor Access", "Welcome Visitor! You can now view the screen.")
                display_visitor_window(root)
            else:
                messagebox.showerror("Login Failed", "Incorrect code for visitor access.")

    for widget in root.winfo_children():
        widget.destroy()

    if user_type == "visitor":
        label_code = tk.Label(root, text="Code:", font=("Arial", 14), bg="#f0f0f0")
        label_code.pack(pady=10)

        entry_code = tk.Entry(root, font=("Arial", 14))
        entry_code.pack(pady=10)

        login_button = tk.Button(root, text="Login", command=lambda: check_login(), font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", width=15)
        login_button.pack(pady=20)
    else:
        label_user = tk.Label(root, text="Username:", font=("Arial", 14), bg="#f0f0f0")
        label_user.pack(pady=10)

        entry_user = tk.Entry(root, font=("Arial", 14))
        entry_user.pack(pady=10)

        label_pass = tk.Label(root, text="Password:", font=("Arial", 14), bg="#f0f0f0")
        label_pass.pack(pady=10)

        entry_pass = tk.Entry(root, show="*", font=("Arial", 14))
        entry_pass.pack(pady=10)

        login_button = tk.Button(root, text="Login", command=lambda: check_login(), font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", width=15)
        login_button.pack(pady=20)

    def go_back():
        display_user_type_selection(root)

    back_button = tk.Button(root, text="Back", command=go_back, font=("Arial", 14), bg="#FF5733", fg="white", relief="raised", width=15)
    back_button.pack(pady=20)

def display_user_type_selection(root):
    for widget in root.winfo_children():
        widget.destroy()

    user_type_var = tk.StringVar(value="admin")

    login_choice_window = tk.Frame(root)
    login_choice_window.pack(fill="both", expand=True)

    admin_radio = tk.Radiobutton(login_choice_window, text="Admin", variable=user_type_var, value="admin", font=("Arial", 16), bg="#f0f0f0")
    admin_radio.pack(pady=20)

    member_radio = tk.Radiobutton(login_choice_window, text="Member", variable=user_type_var, value="member", font=("Arial", 16), bg="#f0f0f0")
    member_radio.pack(pady=20)

    visitor_radio = tk.Radiobutton(login_choice_window, text="Visitor", variable=user_type_var, value="visitor", font=("Arial", 16), bg="#f0f0f0")
    visitor_radio.pack(pady=20)

    login_button = tk.Button(login_choice_window, text="Login", command=lambda: login_window(user_type_var.get(), root), font=("Arial", 16), bg="#4CAF50", fg="white", relief="raised", width=20)
    login_button.pack(pady=30)

def display_admin_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    admin_window = tk.Frame(root)
    admin_window.pack(fill="both", expand=True)

    member_ip = socket.gethostbyname(socket.gethostname())
    
    if member_ip != admin_ip:
        label_ip = tk.Label(admin_window, text=f"Member IP: {member_ip}", font=("Arial", 16), bg="#f0f0f0")
        label_ip.pack(pady=20)
    else:
        label_ip = tk.Label(admin_window, text="Member IP: Localhost (Same machine as Admin)", font=("Arial", 16), bg="#f0f0f0")
        label_ip.pack(pady=20)

    def control_member():
        threading.Thread(target=control_member_thread).start()

    control_button = tk.Button(admin_window, text="Control Member", command=control_member, font=("Arial", 16), bg="#4CAF50", fg="white", relief="raised", width=20)
    control_button.pack(pady=30)

    def logout():
        display_user_type_selection(root)

    logout_button = tk.Button(admin_window, text="Logout", command=logout, font=("Arial", 16), bg="#FF5733", fg="white", relief="raised", width=20)
    logout_button.pack(pady=20)

def display_member_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    member_window = tk.Frame(root)
    member_window.pack(fill="both", expand=True)

    def close_control():
        messagebox.showinfo("Control", "Admin control has been stopped.")
        root.quit()

    close_button = tk.Button(member_window, text="Stop Admin Control", command=close_control, font=("Arial", 16), bg="#FF5733", fg="white", relief="raised", width=20)
    close_button.pack(pady=50)

    def logout():
        display_user_type_selection(root)

    logout_button = tk.Button(member_window, text="Logout", command=logout, font=("Arial", 16), bg="#FF5733", fg="white", relief="raised", width=20)
    logout_button.pack(pady=20)

def display_visitor_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    visitor_window = tk.Frame(root)
    visitor_window.pack(fill="both", expand=True)

    canvas = tk.Canvas(visitor_window, width=1000, height=800)
    canvas.pack()

    def update_screen():
        img = ImageGrab.grab()
        img_np = np.array(img)
        img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        img_tk = ImageTk.PhotoImage(image=Image.fromarray(img_rgb))

        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.img_tk = img_tk
        root.after(100, update_screen)

    update_screen()

    def logout():
        display_user_type_selection(root)

    logout_button = tk.Button(visitor_window, text="Logout", command=logout, font=("Arial", 16), bg="#FF5733", fg="white", relief="raised", width=20)
    logout_button.pack(pady=20)

def start_login():
    root = tk.Tk()
    root.title("Lewis Remote Desktop")
    root.geometry("500x400")
    root.configure(bg="#f0f0f0")

    display_user_type_selection(root)

    root.mainloop()

start_login()


