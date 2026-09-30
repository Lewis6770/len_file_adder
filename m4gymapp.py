"""import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os
import json

# --- Data and Helpers ---

# Sample exercises with image filenames (lowercase, underscores)
EXERCISES = [
    "Incline Bench Press",
    "Bayesian Curls",
    "Weighted Dips",
    "Spider Curls",
    "Chest Press Machine",
    "Hammer Curls",
    "Barbell Back Squat",
    "Leg Press",
    "Leg Extensions",
    "Lying Leg Curls",
    "Seated Calf Raises",
    "Neutral-Grip Chin-Ups",
    "Pull-ups",
    "Tricep Pushdowns",
    "Cable Rows",
    "Skull Crushers",
    "Weighted Back Extensions",
    "Lateral Raises",
    "Front Rope Pulls",
    "Rear Delt Raises",
    "Leg Raises",
    "Plank Hold",
    "Weighted Sit-Ups",
    "Knee Pulls"
]

LEVELS = [
    ("Basic", "levels/basic.png"),
    ("Intermediate", "levels/intermediate.png"),
    ("Good", "levels/good.png"),
    ("Advanced", "levels/advanced.png"),
    ("Insane", "levels/insane.png"),
    ("Elite", "levels/elite.png")
]

USERS_FILE = "users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def load_exercise_image(name):
    # Normalize name to filename style
    fname = name.lower().replace(" ", "_") + ".png"
    path = os.path.join("machine_images", fname)
    try:
        img = Image.open(path).resize((50, 50), Image.ANTIALIAS)
    except Exception:
        # Default image placeholder
        img = Image.new("RGBA", (50, 50), (200, 200, 200, 255))
    return ImageTk.PhotoImage(img)


def load_level_images():
    level_imgs = {}
    for level_name, path in LEVELS:
        try:
            img = Image.open(path).resize((30, 30), Image.ANTIALIAS)
        except Exception:
            img = Image.new("RGBA", (30, 30), (100, 100, 100, 255))
        level_imgs[level_name] = ImageTk.PhotoImage(img)
    return level_imgs


def rank_lift(weight, reps, age, bodyweight):
    # Simple ranking logic - just demo. Real formula can be complex.
    score = (weight * reps) / bodyweight * (1 + (age / 100))
    if score < 1:
        return "Basic"
    elif score < 2:
        return "Intermediate"
    elif score < 3:
        return "Good"
    elif score < 4:
        return "Advanced"
    elif score < 5:
        return "Insane"
    else:
        return "Elite"


# --- Main App Class ---

class M4GymRankingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("M4 Gym Ranking")
        self.geometry("900x700")
        self.resizable(False, False)
        self.users = load_users()
        self.current_user = None
        self.level_images = load_level_images()
        self.exercise_images_cache = {}
        self.create_login_screen()

    # ------ Login Screen ------

    def create_login_screen(self):
        self.clear_window()
        frame = ttk.Frame(self, padding=30)
        frame.pack(expand=True)

        ttk.Label(frame, text="M4 Gym Ranking Login", font=("Segoe UI", 24, "bold")).pack(pady=10)

        ttk.Label(frame, text="Username").pack(anchor="w")
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack()

        ttk.Label(frame, text="Password").pack(anchor="w", pady=(10, 0))
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.pack()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Login", command=self.handle_login).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Create Account", command=self.create_account).grid(row=0, column=1, padx=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Preset Lewis account
        if username == "Lewis" and password == "m4":
            self.current_user = {"username": "Lewis", "routine": self.get_lewis_routine()}
            self.create_main_screen()
            return

        # Check in saved users
        user = self.users.get(username)
        if user and user.get("password") == password:
            self.current_user = user
            self.create_main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_account(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Enter username and password to create account")
            return
        if username in self.users or username == "Lewis":
            messagebox.showerror("Error", "Username taken")
            return
        # Create new user with empty routine
        self.users[username] = {"username": username, "password": password, "routine": []}
        save_users(self.users)
        messagebox.showinfo("Success", "Account created! Now login.")

    # --- Lewis Routine Prebuilt ---
    def get_lewis_routine(self):
        return [
            {"day": "Monday – Chest & Biceps", "exercises": [
                {"name": "Incline Bench Press", "reps": "6–8", "weight": "17.5 + 2.5 kg/side"},
                {"name": "Bayesian Curls", "reps": "8–12", "weight": "7.5 kg/side"},
                {"name": "Weighted Dips", "reps": "6–8", "weight": "Bodyweight or +2.5–5 kg"},
                {"name": "Spider Curls", "reps": "8–12", "weight": "5 + 2.5 kg/side"},
                {"name": "Chest Press Machine", "reps": "6–8", "weight": "75 kg"},
                {"name": "Hammer Curls", "reps": "8–12", "weight": "10–12.5 kg/side"},
            ]},
            {"day": "Tuesday – Legs", "exercises": [
                {"name": "Barbell Back Squat", "reps": "3–6", "weight": "72.5 kg"},
                {"name": "Leg Press", "reps": "3–6", "weight": "230kg/side"},
                {"name": "Leg Extensions", "reps": "3–6", "weight": "57.5 kg"},
                {"name": "Lying Leg Curls", "reps": "3–6", "weight": "55 kg"},
                {"name": "Seated Calf Raises", "reps": "12–15", "weight": "40–50 kg"},
            ]},
            {"day": "Wednesday – Back & Triceps", "exercises": [
                {"name": "Neutral-Grip Chin-Ups", "reps": "6–8", "weight": "bodyweight"},
                {"name": "Pull-ups", "reps": "6–8", "weight": "70 kg"},
                {"name": "Tricep Pushdowns", "reps": "6–8", "weight": "27.5 kg"},
                {"name": "Cable Rows", "reps": "6–8", "weight": "35"},
                {"name": "Skull Crushers", "reps": "6–8", "weight": "5 + 2.5 kg/side"},
                {"name": "Weighted Back Extensions", "reps": "10–15", "weight": "10–20 kg plate"},
            ]},
            {"day": "Thursday – Chest & Biceps", "exercises": [
                {"name": "Incline Dumbbell Press", "reps": "6–8", "weight": "22kg/side"},
                {"name": "Bayesian Curls", "reps": "8–12", "weight": "12.5 kg/side"},
                {"name": "Weighted Dips", "reps": "6–8", "weight": "Bodyweight or +2.5–5 kg"},
                {"name": "Spider Curls", "reps": "8–12", "weight": "5 + 2.5 kg/side"},
                {"name": "Chest Press Machine", "reps": "6–8", "weight": "75 kg"},
                {"name": "Hammer Curls", "reps": "8–12", "weight": "10–12.5 kg/side"},
            ]},
            {"day": "Friday – Legs", "exercises": [
                {"name": "Barbell Back Squat", "reps": "3–6", "weight": "72.5 kg"},
                {"name": "Leg Press", "reps": "3–6", "weight": "5×20 + 10 + 5 kg/side"},
                {"name": "Leg Extensions", "reps": "3–6", "weight": "57.5 kg"},
                {"name": "Lying Leg Curls", "reps": "3–6", "weight": "55 kg"},
                {"name": "Seated Calf Raises", "reps": "12–15", "weight": "40–50 kg"},
            ]},
            {"day": "Saturday – Chest & Shoulders", "exercises": [
                {"name": "Incline Dumbbell Press", "reps": "6–8", "weight": "22kg/side"},
                {"name": "Lateral Raises", "reps": "6–8", "weight": "8 kg/side"},
                {"name": "Weighted Dips", "reps": "6–8", "weight": "Bodyweight or +2.5–5 kg"},
                {"name": "Front Rope Pulls", "reps": "6–8", "weight": "10 kg"},
                {"name": "Chest Press Machine", "reps": "6–8", "weight": "75 kg"},
                {"name": "Tricep Pushdowns", "reps": "6–8", "weight": ""},
                {"name": "Rear Delt Raises", "reps": "10–15", "weight": "5–7 kg/side"},
                {"name": "Skull Crushers", "reps": "6–8", "weight": ""}
            ]},
            {"day": "Sunday – Rest & Recovery", "exercises": []}
        ]

    # ------ Main Screen ------

    def create_main_screen(self):
        self.clear_window()

        header = ttk.Frame(self, padding=10)
        header.pack(fill="x")

        ttk.Label(header, text=f"Welcome, {self.current_user['username']}", font=("Segoe UI", 18, "bold")).pack(
            side="left")
        ttk.Button(header, text="Logout", command=self.logout).pack(side="right")

        # Tabs for Routine and Rank Lifts
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        self.create_routine_tab()
        self.create_rank_lift_tab()

    def logout(self):
        self.current_user = None
        self.create_login_screen()

    def create_routine_tab(self):
        self.routine_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.routine_tab, text="My Routine")

        # Routine display frame with scrollbar
        container = ttk.Frame(self.routine_tab)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.routine_frame = ttk.Frame(canvas)

        self.routine_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.routine_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load routine or empty
        self.display_routine()

        # Button to add exercises for non-Lewis users
        if self.current_user['username'] != "Lewis":
            add_btn = ttk.Button(self.routine_tab, text="Add Exercise", command=self.add_exercise_popup)
            add_btn.pack(pady=10)

    def display_routine(self):
        for widget in self.routine_frame.winfo_children():
            widget.destroy()

        routine = self.current_user.get("routine", [])
        if not routine:
            ttk.Label(self.routine_frame, text="No routine set. Use 'Add Exercise' to create your routine.",
                      font=("Segoe UI", 14)).pack(pady=20)
            return

        for day in routine:
            day_frame = ttk.LabelFrame(self.routine_frame, text=day["day"], padding=10)
            day_frame.pack(fill="x", pady=8)

            for ex in day.get("exercises", []):
                row = ttk.Frame(day_frame)
                row.pack(fill="x", pady=4)

                # Exercise image
                img = self.get_cached_exercise_image(ex["name"])
                lbl_img = ttk.Label(row, image=img)
                lbl_img.image = img
                lbl_img.pack(side="left", padx=5)

                # Exercise name and details
                info = f"{ex['name']} - {ex.get('reps', '')} reps - {ex.get('weight', '')}"
                ttk.Label(row, text=info, font=("Segoe UI", 12)).pack(side="left", padx=10)

    def get_cached_exercise_image(self, name):
        if name not in self.exercise_images_cache:
            self.exercise_images_cache[name] = load_exercise_image(name)
        return self.exercise_images_cache[name]

    def add_exercise_popup(self):
        # Popup for adding exercise to routine (simple implementation)
        day_names = [d["day"] for d in self.current_user.get("routine", [])]
        if not day_names:
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        popup = tk.Toplevel(self)
        popup.title("Add Exercise")
        popup.geometry("400x300")

        ttk.Label(popup, text="Select Day").pack(pady=5)
        day_var = tk.StringVar(value=day_names[0])
        day_menu = ttk.Combobox(popup, textvariable=day_var, values=day_names, state="readonly")
        day_menu.pack()

        ttk.Label(popup, text="Exercise Name").pack(pady=5)
        ex_entry = ttk.Combobox(popup, values=EXERCISES, state="readonly")
        ex_entry.pack()

        ttk.Label(popup, text="Reps").pack(pady=5)
        reps_entry = ttk.Entry(popup)
        reps_entry.pack()

        ttk.Label(popup, text="Weight").pack(pady=5)
        weight_entry = ttk.Entry(popup)
        weight_entry.pack()

        def add_exercise():
            day = day_var.get()
            name = ex_entry.get()
            reps = reps_entry.get()
            weight = weight_entry.get()
            if not name:
                messagebox.showerror("Error", "Pick an exercise")
                return

            routine = self.current_user.get("routine", [])
            for d in routine:
                if d["day"] == day:
                    d["exercises"].append({"name": name, "reps": reps, "weight": weight})
                    break
            else:
                # Day not found, create new
                routine.append({"day": day, "exercises": [{"name": name, "reps": reps, "weight": weight}]})
            self.current_user["routine"] = routine
            self.users[self.current_user["username"]] = self.current_user
            save_users(self.users)
            self.display_routine()
            popup.destroy()

        ttk.Button(popup, text="Add", command=add_exercise).pack(pady=20)

    # ------ Rank Lift Tab ------

    def create_rank_lift_tab(self):
        self.rank_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.rank_tab, text="Lift Ranking")

        frm = ttk.Frame(self.rank_tab, padding=20)
        frm.pack(expand=True)

        ttk.Label(frm, text="Enter your lift data", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                        pady=10)

        ttk.Label(frm, text="Weight lifted (kg):").grid(row=1, column=0, sticky="e", pady=8)
        self.weight_lifted_entry = ttk.Entry(frm, width=20)
        self.weight_lifted_entry.grid(row=1, column=1, sticky="w", pady=8)

        ttk.Label(frm, text="Reps:").grid(row=2, column=0, sticky="e", pady=8)
        self.reps_entry = ttk.Entry(frm, width=20)
        self.reps_entry.grid(row=2, column=1, sticky="w", pady=8)

        ttk.Label(frm, text="Age:").grid(row=3, column=0, sticky="e", pady=8)
        self.age_entry = ttk.Entry(frm, width=20)
        self.age_entry.grid(row=3, column=1, sticky="w", pady=8)

        ttk.Label(frm, text="Bodyweight (kg):").grid(row=4, column=0, sticky="e", pady=8)
        self.bodyweight_entry = ttk.Entry(frm, width=20)
        self.bodyweight_entry.grid(row=4, column=1, sticky="w", pady=8)

        ttk.Button(frm, text="Calculate Rank", command=self.calculate_rank).grid(row=5, column=0, columnspan=2, pady=20)

        self.rank_result_label = ttk.Label(frm, text="", font=("Segoe UI", 16, "bold"))
        self.rank_result_label.grid(row=6, column=0, columnspan=2, pady=10)

    def calculate_rank(self):
        try:
            weight = float(self.weight_lifted_entry.get())
            reps = int(self.reps_entry.get())
            age = int(self.age_entry.get())
            bodyweight = float(self.bodyweight_entry.get())
        except Exception:
            messagebox.showerror("Error", "Enter valid numeric inputs")
            return

        level = rank_lift(weight, reps, age, bodyweight)
        level_img = self.level_images.get(level)
        if level_img:
            self.rank_result_label.config(text=f"Rank: {level} ", image=level_img, compound="right")
            self.rank_result_label.image = level_img
        else:
            self.rank_result_label.config(text=f"Rank: {level}", image="", compound="none")

    # --- Utility ---

    def clear_window(self):
        for w in self.winfo_children():
            w.destroy()


if __name__ == "__main__":
    app = M4GymRankingApp()
    app.mainloop()"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import json
import time

# ------------------------
# CONFIG
# ------------------------
USERS_FILE = "users.json"
BACKGROUND_IMAGE = "assets/gym_bg.jpg"
FONT_HEADER = ("Segoe UI", 18, "bold")
FONT_NORMAL = ("Segoe UI", 12)
PRIMARY_COLOR = "#1f1f1f"
ACCENT_COLOR = "#e63946"

EXERCISES = ["Bench Press", "Squat", "Deadlift", "Pull-Ups", "Incline Press", "Barbell Row", "Leg Press"]

AVERAGE_LIFTS = {
    "Bench Press": {"male": 1.0, "female": 0.6},
    "Squat": {"male": 1.5, "female": 1.0},
    "Deadlift": {"male": 1.8, "female": 1.2},
    "Pull-Ups": {"male": 0.8, "female": 0.4},
    "Incline Press": {"male": 0.9, "female": 0.5},
    "Barbell Row": {"male": 1.2, "female": 0.8},
    "Leg Press": {"male": 2.0, "female": 1.5}
}

# ------------------------
# Helpers
# ------------------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def calculate_rank_level(score):
    if score < 0.8:
        return "Basic"
    elif score < 1.1:
        return "Intermediate"
    elif score < 1.4:
        return "Good"
    elif score < 1.7:
        return "Advanced"
    elif score < 2.0:
        return "Insane"
    else:
        return "Elite"

# ------------------------
# Main App
# ------------------------
class M4GymApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("M4 Gym Upgrade")
        self.geometry("1000x700")
        self.resizable(False, False)
        self.users = load_users()
        self.current_user = None

        self.background_label = None
        self.init_styles()
        self.setup_background()
        self.show_login()

    def init_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", font=FONT_NORMAL, background=PRIMARY_COLOR, foreground="white")
        style.configure("TButton", font=FONT_NORMAL, background=ACCENT_COLOR, foreground="white", padding=6)
        style.configure("TFrame", background=PRIMARY_COLOR)
        style.configure("TNotebook", background=PRIMARY_COLOR)
        style.configure("TNotebook.Tab", font=FONT_NORMAL, padding=10)
        style.configure("Custom.TCombobox", fieldbackground="#333", background="#222", foreground="white")

    def setup_background(self):
        if os.path.exists(BACKGROUND_IMAGE):
            bg_img = Image.open(BACKGROUND_IMAGE)
            bg_img = bg_img.resize((1000, 700), Image.ANTIALIAS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            self.background_label = tk.Label(self, image=self.bg_photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def show_login(self):
        self.clear_window()

        frame = ttk.Frame(self, padding=30)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Welcome to M4 Gym App", font=FONT_HEADER).pack(pady=10)
        ttk.Label(frame, text="Username:").pack()
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack()

        ttk.Label(frame, text="Password:").pack(pady=(10, 0))
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.pack()

        ttk.Button(frame, text="Login", command=self.handle_login).pack(pady=10)
        ttk.Button(frame, text="Create Account", command=self.create_account).pack()

    def handle_login(self):
        u = self.username_entry.get().strip()
        p = self.password_entry.get().strip()
        if u in self.users and self.users[u]['password'] == p:
            self.current_user = self.users[u]
            self.show_main_ui()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_account(self):
        u = self.username_entry.get().strip()
        p = self.password_entry.get().strip()
        if u in self.users:
            messagebox.showerror("Error", "Username already exists")
            return
        self.users[u] = {
            "password": p,
            "routine": [
                {"name": "Bench Press", "sets": 4, "reps": 8},
                {"name": "Squat", "sets": 4, "reps": 6},
                {"name": "Deadlift", "sets": 3, "reps": 5}
            ],
            "history": [],
            "profile": {"goal": "Strength", "age": 18, "weight": 70, "name": u}
        }
        save_users(self.users)
        messagebox.showinfo("Success", "Account created! Please login.")

    def show_main_ui(self):
        self.clear_window()

        header = ttk.Frame(self, padding=10)
        header.pack(fill="x")
        ttk.Label(header, text=f"Welcome, {self.current_user['profile'].get('name', 'User')}", font=FONT_HEADER).pack(side="left")
        ttk.Button(header, text="Logout", command=self.logout).pack(side="right")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill="both", padx=10, pady=10)

        self.routine_tab = ttk.Frame(self.tabs)
        self.rank_tab = ttk.Frame(self.tabs)
        self.profile_tab = ttk.Frame(self.tabs)
        self.export_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.routine_tab, text="🏋️ Routine")
        self.tabs.add(self.rank_tab, text="📈 Rank Lift")
        self.tabs.add(self.profile_tab, text="👤 Profile")
        self.tabs.add(self.export_tab, text="📤 Export")

        self.build_routine_tab()
        self.build_rank_tab()
        self.build_profile_tab()
        self.build_export_tab()

    def build_rank_tab(self):
        frame = ttk.Frame(self.rank_tab, padding=20)
        frame.pack(pady=10)

        ttk.Label(frame, text="🏋️ Select Exercise:").grid(row=0, column=0, sticky="e", pady=5)
        self.exercise_var = tk.StringVar(value=EXERCISES[0])
        self.exercise_cb = ttk.Combobox(frame, values=EXERCISES, textvariable=self.exercise_var, state="readonly", style="Custom.TCombobox")
        self.exercise_cb.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="🔩 Weight Lifted (kg):").grid(row=1, column=0, sticky="e", pady=5)
        self.lift_entry = ttk.Entry(frame)
        self.lift_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="🔁 Reps:").grid(row=2, column=0, sticky="e", pady=5)
        self.reps_entry = ttk.Entry(frame)
        self.reps_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="📅 Age:").grid(row=3, column=0, sticky="e", pady=5)
        self.age_entry = ttk.Entry(frame)
        self.age_entry.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="⚖️ Bodyweight (kg):").grid(row=4, column=0, sticky="e", pady=5)
        self.bw_entry = ttk.Entry(frame)
        self.bw_entry.grid(row=4, column=1, pady=5)

        ttk.Button(frame, text="🔍 Calculate Rank", command=self.calculate_rank).grid(row=5, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(frame, text="", font=("Segoe UI", 12, "bold"))
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

    def calculate_rank(self):
        try:
            exercise = self.exercise_var.get()
            weight = float(self.lift_entry.get())
            reps = int(self.reps_entry.get())
            age = int(self.age_entry.get())
            bw = float(self.bw_entry.get())

            ratio = (weight * reps) / bw
            average = AVERAGE_LIFTS.get(exercise, {"male": 1.0})["male"]
            level = calculate_rank_level(ratio)

            self.result_label.config(
                text=f"🏆 {exercise}\nLevel: {level}\nYour Ratio: {ratio:.2f}\nAverage: {average:.2f}x BW")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def build_routine_tab(self):
        ttk.Label(self.routine_tab, text="(Routine Editor coming next)").pack(pady=50)

    def build_profile_tab(self):
        ttk.Label(self.profile_tab, text="(Profile Editor coming next)").pack(pady=50)

    def build_export_tab(self):
        ttk.Label(self.export_tab, text="(Export Features coming next)").pack(pady=50)

    def logout(self):
        self.current_user = None
        self.show_login()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = M4GymApp()
    app.mainloop()
