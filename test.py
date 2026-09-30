import tkinter as tk

def main():
    # Create the main window
    root = tk.Tk()
    root.title("My Tkinter App")
    root.geometry("400x300")
    
    # Create a label
    label = tk.Label(root, text="Hello, World!", font=("Arial", 14))
    label.pack(pady=20)
    
    # Create a button
    button = tk.Button(root, text="Click Me", command=lambda: print("Button clicked!"))
    button.pack(pady=10)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
