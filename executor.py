import tkinter as tk
from tkinter import filedialog, messagebox
import getpass
import psutil  # To check running processes

# App state
injected = False
injected_accounts = []
pre_scripts = {
    "Fly Script": "game.Players.LocalPlayer.Character.HumanoidRootPart.Velocity = Vector3.new(0,50,0)",
    "Speed Script": "game.Players.LocalPlayer.Character.Humanoid.WalkSpeed = 100"
}

# Function to check if Roblox is running and in a game
def is_roblox_in_game():
    # Loop through all processes to check if Roblox is running
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            if 'RobloxPlayerBeta.exe' in proc.info['name']:  # Check for the Roblox client
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# Functions
def save_file():
    file = filedialog.asksaveasfile(defaultextension=".txt",
                                     filetypes=[("Text Files", "*.txt")])
    if file:
        file.write(text_area.get(1.0, tk.END))
        file.close()

def open_file():
    file = filedialog.askopenfile(defaultextension=".txt",
                                   filetypes=[("Text Files", "*.txt")])
    if file:
        content = file.read()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, content)
        file.close()

def clear_text():
    if messagebox.askyesno("Clear", "Are you sure you want to clear all text?"):
        text_area.delete(1.0, tk.END)

def inject():
    global injected
    if not is_roblox_in_game():
        messagebox.showwarning("Inject", "You must be in a Roblox game to inject!")
        return

    if not injected:
        roblox_user = getpass.getuser()  # simulate system username as Roblox user
        injected_accounts.append(roblox_user)
        injected = True
        messagebox.showinfo("Injected", f"Injected into Roblox as {roblox_user} 💉")
    else:
        messagebox.showinfo("Already Injected", "Already injected into Roblox.")

def show_injected_accounts():
    if injected_accounts:
        accounts_str = "\n".join(f"• {acc}" for acc in injected_accounts)
        messagebox.showinfo("Injected Accounts", f"Active Injected Accounts:\n\n{accounts_str}")
    else:
        messagebox.showinfo("Injected Accounts", "No accounts injected.")

def show_pre_scripts():
    text = ""
    for name, script in pre_scripts.items():
        text += f"{name}:\n{script}\n\n"
    messagebox.showinfo("Pre-Made Scripts", text.strip())

def execute_script():
    if not injected:
        messagebox.showwarning("Execute", "Please inject into Roblox first (💉)!")  
        return

    code = text_area.get(1.0, tk.END)
    if code.strip():
        messagebox.showinfo("Execute", "Lua script executed (with loadstring support):\n" + code)
    else:
        messagebox.showwarning("Execute", "No code to execute!")

# Draggable functions
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

# GUI setup
root = tk.Tk()
root.title("Niks Executer (Lite)")
root.geometry("800x500")

# Remove OS window frame
root.overrideredirect(True)

# Top bar frame
top_bar = tk.Frame(root, bg="#2c2f33", height=40)
top_bar.pack(fill="x")

# Draggable events
top_bar.bind("<ButtonPress-1>", start_move)
top_bar.bind("<ButtonRelease-1>", stop_move)
top_bar.bind("<B1-Motion>", do_move)

# Left-side buttons
tk.Button(top_bar, text="Settings", bg="#7289da", fg="white", command=lambda: messagebox.showinfo("Settings", "No settings yet")).pack(side="left", padx=2, pady=5)
tk.Button(top_bar, text="Open Folder", command=open_file).pack(side="left", padx=2)
tk.Button(top_bar, text="Save", command=save_file).pack(side="left", padx=2)
tk.Button(top_bar, text="Clear", command=clear_text).pack(side="left", padx=2)

# Spacer
tk.Label(top_bar, text="", bg="#2c2f33").pack(side="left", expand=True)

# Right-side buttons
tk.Button(top_bar, text=">", font=("Arial", 12, "bold"), bg="#43b581", fg="white", command=execute_script).pack(side="right", padx=4)
tk.Button(top_bar, text="📺 4TVS", bg="#99aab5", command=show_injected_accounts).pack(side="right", padx=2)
tk.Button(top_bar, text="Pre-Scripts", command=show_pre_scripts).pack(side="right", padx=2)
tk.Button(top_bar, text="💉", font=("Arial", 12), command=inject).pack(side="right", padx=2)

# Custom close button (X)
tk.Button(top_bar, text="✕", bg="#ff5c5c", fg="white", command=root.quit).pack(side="right", padx=2)

# Text area
text_area = tk.Text(root, wrap=tk.WORD, font=("Consolas", 12), bg="black", fg="white", insertbackground="white")
text_area.pack(expand=True, fill='both')

# Run app
root.mainloop()
# delete this after you put it in Visual Studio code or Python