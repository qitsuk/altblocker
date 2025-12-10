import tkinter as tk
from tkinter import ttk
import keyboard
import threading
import pystray
from PIL import Image, ImageDraw
import subprocess
import sys
import json
import os
import ctypes
import winshell
from win32com.client import Dispatch

alt_blocked = True
tray_icon = None

__version__ = "0.12.0"

# Config file path
def get_config_path():
    if getattr(sys, 'frozen', False):
        app_dir = os.path.dirname(sys.executable)
    else:
        app_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(app_dir, 'alt_blocker_config.json')

def load_config():
    try:
        with open(get_config_path(), 'r') as f:
            return json.load(f)
    except:
        return {'start_with_windows': False, 'start_minimized': False}

def save_config():
    config = {
        'start_with_windows': start_with_windows.get(),
        'start_minimized': start_minimized.get()
    }
    try:
        with open(get_config_path(), 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving config: {e}")

def toggle_alt():
    global alt_blocked
    alt_blocked = not alt_blocked
    if alt_blocked:
        keyboard.block_key('alt')
        update_ui_blocked()
    else:
        keyboard.unblock_key('alt')
        update_ui_unblocked()
    update_tray_icon()

def update_ui_blocked():
    status_frame.config(bg="#ef4444")
    status_label.config(text="Alt-tasten er blokeret", bg="#ef4444", fg="white")
    status_icon.config(text="🔒", bg="#ef4444")
    toggle_button.config(text="Fjern blokering", bg="#dc2626", activebackground="#b91c1c")

def update_ui_unblocked():
    status_frame.config(bg="#10b981")
    status_label.config(text="Alt-tasten er aktiv", bg="#10b981", fg="white")
    status_icon.config(text="✓", bg="#10b981")
    toggle_button.config(text="Blokér Alt-tasten", bg="#059669", activebackground="#047857")

def create_icon(color):
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((8, 8, 56, 56), fill=color)
    return img

def update_tray_icon():
    if tray_icon:
        tray_icon.icon = create_icon((239, 68, 68, 255) if alt_blocked else (16, 185, 129, 255))
        tray_icon.title = "Alt blokeret" if alt_blocked else "Alt er aktiv"

def show_window(icon=None, item=None):
    root.after(0, root.deiconify)

def quit_app(icon=None, item=None):
    if tray_icon:
        tray_icon.stop()
    root.quit()

def hide_window():
    root.withdraw()
    global tray_icon
    if tray_icon is None:
        color = (239, 68, 68, 255) if alt_blocked else (16, 185, 129, 255)
        image = create_icon(color)
        menu = pystray.Menu(
            pystray.MenuItem("Vis vindue", show_window, default=True),
            pystray.MenuItem("Afslut", quit_app)
        )
        tray_icon = pystray.Icon("Alt Blocker", image, "Alt Blocker", menu)
        threading.Thread(target=tray_icon.run, daemon=True).start()
    else:
        update_tray_icon()

# --- SHORTCUT-ONLY STARTUP (NO SCHEDULED TASKS) ---

def enable_start_with_windows():
    startup = winshell.startup()
    shortcut_path = os.path.join(startup, "AltBlocker.lnk")

    if getattr(sys, 'frozen', False):
        target = sys.executable
        args = ""
    else:
        target = sys.executable
        args = sys.argv[0]

    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.Arguments = args
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.IconLocation = target
        shortcut.save()
    except Exception as e:
        print(f"Error creating shortcut: {e}")

def disable_start_with_windows():
    try:
        startup = winshell.startup()
        shortcut_path = os.path.join(startup, "AltBlocker.lnk")
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
    except Exception as e:
        print(f"Error removing shortcut: {e}")

def toggle_start_with_windows():
    if start_with_windows.get():
        enable_start_with_windows()
    else:
        disable_start_with_windows()
    save_config()

def on_start_minimized_toggle():
    save_config()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         font=("Segoe UI", 9))
        label.pack(ipadx=5, ipady=2)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

# GUI Setup
root = tk.Tk()
root.title(f"Alt Blocker v{__version__}")
root.geometry("400x650")
root.configure(bg="#1e293b")
root.resizable(False, False)

try:
    if getattr(sys, 'frozen', False):
        icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
    else:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
except:
    pass

config = load_config()
start_with_windows = tk.BooleanVar(master=root, value=config['start_with_windows'])
start_minimized = tk.BooleanVar(master=root, value=config['start_minimized'])

header = tk.Frame(root, bg="#0f172a", height=80)
header.pack(fill="x")
header.pack_propagate(False)

title = tk.Label(header, text="Alt Blocker", font=("Segoe UI", 20, "bold"),
                 bg="#0f172a", fg="#e2e8f0")
title.pack(pady=25)

main_container = tk.Frame(root, bg="#1e293b")
main_container.pack(fill="both", expand=True, padx=20, pady=20)

status_frame = tk.Frame(main_container, bg="#ef4444")
status_frame.pack(fill="x", pady=(0, 20))

status_content = tk.Frame(status_frame, bg="#ef4444")
status_content.pack(pady=20)

status_icon = tk.Label(status_content, text="🔒", font=("Segoe UI", 32),
                       bg="#ef4444", fg="white")
status_icon.pack()

status_label = tk.Label(status_content, text="Alt-tasten er blokeret",
                        font=("Segoe UI", 14, "bold"), bg="#ef4444", fg="white")
status_label.pack(pady=(5, 0))

toggle_button = tk.Button(main_container, text="Fjern blokering",
                          command=toggle_alt, font=("Segoe UI", 11, "bold"),
                          bg="#dc2626", fg="white", relief="flat",
                          padx=30, pady=12)
toggle_button.pack(fill="x", pady=(0, 10))

tray_button = tk.Button(main_container, text="Minimér til systembakke",
                        command=hide_window, font=("Segoe UI", 11),
                        bg="#334155", fg="#e2e8f0", relief="flat",
                        padx=30, pady=12)
tray_button.pack(fill="x", pady=(0, 20))

settings_frame = tk.Frame(main_container, bg="#2d3748")
settings_frame.pack(fill="x", pady=(0, 20))

settings_title = tk.Label(settings_frame, text="Indstillinger",
                          font=("Segoe UI", 11, "bold"),
                          bg="#2d3748", fg="#e2e8f0")
settings_title.pack(anchor="w", padx=15, pady=(15, 10))

separator = tk.Frame(settings_frame, bg="#4a5568", height=1)
separator.pack(fill="x", padx=15)

cb_start_windows = tk.Checkbutton(settings_frame, text="Start med Windows",
                                   variable=start_with_windows,
                                   command=toggle_start_with_windows,
                                   bg="#2d3748", fg="#e2e8f0",
                                   font=("Segoe UI", 10),
                                   selectcolor="#2d3748", cursor="hand2")
cb_start_windows.pack(anchor="w", padx=15, pady=(10, 5))

cb_start_minimized = tk.Checkbutton(settings_frame, text="Start minimeret til systembakke",
                                     variable=start_minimized,
                                     command=on_start_minimized_toggle,
                                     bg="#2d3748", fg="#e2e8f0",
                                     font=("Segoe UI", 10),
                                     selectcolor="#2d3748", cursor="hand2")
cb_start_minimized.pack(anchor="w", padx=15, pady=(5, 15))

exit_button = tk.Button(main_container, text="Afslut",
                        command=quit_app, font=("Segoe UI", 10),
                        bg="#374151", fg="#9ca3af",
                        relief="flat", padx=30, pady=10)
exit_button.pack(fill="x", pady=(10, 0))

keyboard.block_key('alt')

if start_minimized.get():
    root.after(100, hide_window)

def on_closing():
    hide_window()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
