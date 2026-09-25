import tkinter as tk
from tkinter import ttk
import random
import json
import os
import platform

# ==========================================
# 0. CROSS-PLATFORM AUDIO SYSTEM
# ==========================================
def play_sfx(sfx_type):
    """Plays custom pitch-based sound effects without external libraries."""
    try:
        if platform.system() == "Windows":
            import winsound
            if sfx_type == "success":
                winsound.Beep(1200, 80)  # High sci-fi chirp
                winsound.Beep(1800, 100)
            elif sfx_type == "error":
                winsound.Beep(300, 200)  # Low error buzz
            elif sfx_type == "warp":
                winsound.Beep(800, 50)
                winsound.Beep(600, 50)
                winsound.Beep(400, 80)
            else:
                winsound.Beep(1000, 60)
        else:
            # Mac/Linux fallback using system bell sequences
            root.bell()
    except Exception:
        root.bell()

# ==========================================
# 1. SETUP THE MATH, UNITS & THEMES
# ==========================================
UNITS = {
    "Terameter (Tm)": 12,
    "Gigameter (Gm)": 9,
    "Megameter (Mm)": 6,
    "Kilometer (km)": 3,
    "Meter (m)": 0,
    "Decimeter (dm)": -1,
    "Centimeter (cm)": -2,
    "Millimeter (mm)": -3,
    "Micrometer (μm)": -6,
    "Nanometer (nm)": -9,
    "Picometer (pm)": -12,
    "Femtometer (fm)": -15
}
unit_names = list(UNITS.keys())

SUPERSCRIPTS = {
    '-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³',
    '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
}

THEMES = {
    "Matrix": {
        "bg": "black", "panel": "#111111", "text": "white", 
        "accent": "#00ffcc", "secondary": "#00ff00", "danger": "#ff003c"
    },
    "Cyberpunk": {
        "bg": "#0f051d", "panel": "#1a0b2e", "text": "#ffffff", 
        "accent": "#00f0ff", "secondary": "#ff007f", "danger": "#ff3366"
    },
    "Deep Space Amber": {
        "bg": "#120800", "panel": "#241300", "text": "#ffe6cc", 
        "accent": "#ffb000", "secondary": "#ff8800", "danger": "#ff3300"
    }
}
current_theme_name = "Matrix"

HS_FILE = "spacetime_highscore.json"

def load_highscore():
    if os.path.exists(HS_FILE):
        try:
            with open(HS_FILE, "r") as f:
                return json.load(f).get("high_streak", 0)
        except:
            return 0
    return 0

def save_highscore(score):
    try:
        with open(HS_FILE, "w") as f:
            json.dump({"high_streak": score}, f)
    except:
        pass

def get_superscript(number_str):
    return "".join(SUPERSCRIPTS.get(char, char) for char in str(number_str))

# ==========================================
# 2. CREATE THE MAIN APP WINDOW & LAYOUT
# ==========================================
root = tk.Tk()
root.title("Space-Time Unit Converter: Quantum Edition")
root.geometry("900x750") 
root.resizable(True, True) 

canvas = tk.Canvas(root, bg=THEMES[current_theme_name]["bg"], highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

sidebar = tk.Frame(root, width=260, bg=THEMES[current_theme_name]["panel"], bd=2, relief="sunken")
sidebar.pack(side="right", fill="y")

# ==========================================
# 3. DRAW STATIC STARS
# ==========================================
def draw_static_stars():
    canvas.delete("static_star")
    for _ in range(800): 
        x = random.randint(0, 2500)
        y = random.randint(0, 1500)
        size = random.choice([1, 1, 2])
        canvas.create_oval(x, y, x+size, y+size, fill="white", outline="", tags="static_star")

draw_static_stars()
easter_egg_text = canvas.create_text(320, 80, text="", font=("Arial", 32, "bold"), fill="#ff3333", width=550, justify="center")

# ==========================================
# 4. STAR WARS HYPERDRIVE ANIMATION
# ==========================================
hyper_stars = []
is_warping = False

def trigger_hyperdrive():
    global is_warping
    if is_warping: 
        return 
    is_warping = True
    canvas.delete("static_star")
    play_sfx("warp")
    
    for _ in range(200):
        line_id = canvas.create_line(300, 325, 300, 325, fill="white", width=2)
        x = random.randint(-2500, 2500)
        y = random.randint(-2500, 2500)
        z = random.randint(100, 1000)
        hyper_stars.append({"id": line_id, "x": x, "y": y, "z": z, "old_z": z})
        
    animate_warp()
    root.after(1200, stop_hyperdrive)

def animate_warp():
    if not is_warping: 
        return
    center_x = root.winfo_width() / 2 - 130 
    center_y = root.winfo_height() / 2
    fov = 300
    speed = 60.0

    for star in hyper_stars:
        star["old_z"] = star["z"]
        star["z"] -= speed
        if star["z"] <= 1:
            star["z"] = 1000
            star["old_z"] = 1000
            star["x"] = random.randint(-2500, 2500)
            star["y"] = random.randint(-2500, 2500)

        px = (star["x"] / star["z"]) * fov + center_x
        py = (star["y"] / star["z"]) * fov + center_y
        old_px = (star["x"] / star["old_z"]) * fov + center_x
        old_py = (star["y"] / star["old_z"]) * fov + center_y
        
        canvas.coords(star["id"], old_px, old_py, px, py)

    root.after(30, animate_warp)

def stop_hyperdrive():
    global is_warping
    is_warping = False
    for star in hyper_stars:
        canvas.delete(star["id"])
    hyper_stars.clear()
    draw_static_stars()

# ==========================================
# 5. MAIN CONVERTER FUNCTIONS
# ==========================================
def do_conversion(event=None):
    input_str = entry_value.get().strip()
    t = THEMES[current_theme_name]
    
    lbl_normal_ans.config(text="0", fg=t["accent"], font=("Courier", 16, "bold"))
    lbl_sci_ans.config(text="0 × 10⁰", fg=t["secondary"], font=("Courier", 22, "bold"))
    canvas.itemconfig(easter_egg_text, text="") 
    
    if not input_str:
        play_sfx("error")
        lbl_normal_ans.config(text="Error", fg=t["danger"])
        lbl_sci_ans.config(text="Field is empty", fg=t["danger"], font=("Arial", 14, "bold"))
        return

    try:
        amount = float(input_str)
    except ValueError:
        play_sfx("error")
        lbl_normal_ans.config(text="Error", fg=t["danger"])
        lbl_sci_ans.config(text="Invalid Input", fg=t["danger"], font=("Arial", 14, "bold"))
        return

    trigger_hyperdrive()

    egg_numbers = [0.67, 6.7, 67.0, 670.0, 6700.0, 67000.0, 670000.0, 6700000.0]
    if amount in egg_numbers:
        canvas.itemconfig(easter_egg_text, text="REALLY IN THE BIG 26 😮‍💨")

    from_unit = combo_from.get()
    to_unit = combo_to.get()
    power_diff = UNITS[from_unit] - UNITS[to_unit] 
    final_answer = amount * (10 ** power_diff)
    
    normal_format = f"{final_answer:.40f}".rstrip('0').rstrip('.')
    if normal_format == "": normal_format = "0"
    
    char_length = len(normal_format)
    if char_length > 35: dynamic_font = ("Courier", 9, "bold")
    elif char_length > 25: dynamic_font = ("Courier", 11, "bold")
    elif char_length > 18: dynamic_font = ("Courier", 13, "bold")
    else: dynamic_font = ("Courier", 16, "bold")
        
    raw_sci = f"{final_answer:e}"           
    sci_parts = raw_sci.split('e')          
    clean_number = sci_parts[0].rstrip('0').rstrip('.') 
    if clean_number == "": clean_number = "0" 
    
    exponent = int(sci_parts[1])
    super_exponent = get_superscript(exponent)
    scientific_format = f"{clean_number} × 10{super_exponent}" 
    
    lbl_normal_ans.config(text=normal_format, fg=t["accent"], font=dynamic_font)
    lbl_sci_ans.config(text=scientific_format, fg=t["secondary"])
    
    history_entry = f"{amount} {from_unit.split()[1]} \n➔ {scientific_format} {to_unit.split()[1]}\n"
    listbox_history.insert(0, history_entry)

def swap_units():
    play_sfx("click")
    temp = combo_from.get()
    combo_from.set(combo_to.get())
    combo_to.set(temp)

def clear_history():
    play_sfx("click")
    listbox_history.delete(0, tk.END)

def change_theme(selected_theme):
    global current_theme_name
    current_theme_name = selected_theme
    t = THEMES[current_theme_name]
    play_sfx("click")
    
    canvas.config(bg=t["bg"])
    sidebar.config(bg=t["panel"])
    ui_frame.config(bg=t["panel"])
    
    for widget in ui_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=t["panel"], fg=t["text"])
    lbl_normal_ans.config(bg=t["panel"])
    lbl_sci_ans.config(bg=t["panel"])
    
    for widget in sidebar.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=t["panel"], fg=t["accent"])

# ==========================================
# 6. MISSION: IMPOSSIBLE GAME
# ==========================================
def launch_mission_impossible():
    play_sfx("click")
    game_win = tk.Toplevel(root)
    game_win.title("TERMINAL OVERRIDE - ENDLESS PROTOCOL")
    game_win.geometry("750x600")
    t = THEMES[current_theme_name]
    game_win.config(bg=t["bg"])
    game_win.resizable(False, False)
    game_win.grab_set() 

    diff_var = tk.StringVar(value="Jedi")

    def start_game_loop():
        play_sfx("click")
        diff = diff_var.get()
        diff_frame.destroy()
        run_game_engine(game_win, diff)

    diff_frame = tk.Frame(game_win, bg=t["bg"])
    diff_frame.pack(fill="both", expand=True)

    tk.Label(diff_frame, text="SELECT QUANTUM DIFFICULTY", font=("Courier", 20, "bold"), bg=t["bg"], fg=t["secondary"]).pack(pady=40)
    
    for d_name, d_desc in [("Cadet", "Generous timer (30s), steady pace."), ("Jedi", "Balanced timer (20s), standard security."), ("Quantum Core", "Relentless timer (12s), shrinks each level!")]:
        tk.Radiobutton(diff_frame, text=f"{d_name}: {d_desc}", variable=diff_var, value=d_name, font=("Courier", 12), bg=t["bg"], fg=t["text"], selectcolor=t["panel"]).pack(anchor="w", padx=100, pady=10)

    tk.Button(diff_frame, text="INITIALIZE PROTOCOL", command=start_game_loop, bg=t["accent"], fg="black", font=("Courier", 14, "bold"), width=22).pack(pady=40)

def run_game_engine(game_win, difficulty):
    t = THEMES[current_theme_name]
    for w in game_win.winfo_children():
        w.destroy()
    game_win.config(bg=t["bg"])

    base_time = 30 if difficulty == "Cadet" else (20 if difficulty == "Jedi" else 12)
    state = {"time_left": base_time, "target_exponent": 0, "active": True, "streak": 0, "lives": 3, "difficulty": difficulty}
    high_score = load_highscore()

    lbl_header = tk.Label(game_win, text=f"QUANTUM OVERRIDE [{difficulty.upper()}]", font=("Courier", 18, "bold"), bg=t["bg"], fg=t["danger"])
    lbl_header.pack(pady=10)

    lbl_status = tk.Label(game_win, text=f"STREAK: 0   |   HIGH SCORE: {high_score}   |   LIVES: ♥ ♥ ♥", font=("Courier", 13, "bold"), bg=t["bg"], fg=t["accent"])
    lbl_status.pack(pady=5)

    lbl_timer = tk.Label(game_win, text=f"TIME REMAINING: {base_time}.0s", font=("Courier", 16, "bold"), bg=t["bg"], fg=t["secondary"])
    lbl_timer.pack(pady=10)

    lbl_prompt = tk.Label(game_win, text="", font=("Courier", 12), bg=t["bg"], fg=t["text"], wraplength=680, justify="center")
    lbl_prompt.pack(pady=10)

    entry_ans = tk.Entry(game_win, font=("Courier", 18, "bold"), bg=t["panel"], fg=t["secondary"], insertbackground=t["secondary"], justify="center")
    entry_ans.pack(pady=10)
    entry_ans.focus()

    lbl_feedback = tk.Label(game_win, text="Awaiting input sequence...", font=("Courier", 13, "italic"), bg=t["bg"], fg="gray")
    lbl_feedback.pack(pady=10)

    def update_ui():
        hearts = "♥ " * state["lives"]
        lbl_status.config(text=f"STREAK: {state['streak']}   |   HIGH SCORE: {high_score}   |   LIVES: {hearts}")

    def generate_hack():
        if state["difficulty"] == "Cadet": state["time_left"] = max(10, 30 - state["streak"])
        elif state["difficulty"] == "Jedi": state["time_left"] = max(8, 20 - state["streak"])
        else: state["time_left"] = max(5, 12 - (state["streak"] * 1.5))

        from_u = random.choice(unit_names)
        to_u = random.choice(unit_names)
        while from_u == to_u:
            to_u = random.choice(unit_names)
            
        state["target_exponent"] = UNITS[from_u] - UNITS[to_u]
        
        prompt_text = (
            f"FIREWALL BYPASS ACTIVE.\n"
            f"Solve conversion equation:\n"
            f"1 {from_u} = 10^[?] {to_u}\n"
            f"Enter exact exponent value (e.g. 5 or -5):"
        )
        lbl_prompt.config(text=prompt_text)
        entry_ans.delete(0, tk.END)

    def check_hack(event=None):
        nonlocal high_score
        if not state["active"]: return
        
        user_input = entry_ans.get().strip()
        try:
            user_val = int(user_input)
            if user_val == state["target_exponent"]:
                state["streak"] += 1
                play_sfx("success")
                
                if state["streak"] > high_score:
                    high_score = state["streak"]
                    save_highscore(high_score)

                lbl_feedback.config(text=f"FIREWALL BYPASSED! Streak increased.", fg=t["accent"])
                update_ui()
                generate_hack()
            else:
                state["lives"] -= 1
                play_sfx("error")
                update_ui()
                
                if state["lives"] <= 0:
                    state["active"] = False
                    lbl_header.config(text="MAINFRAME LOCKED", fg=t["danger"])
                    lbl_feedback.config(text=f"FAILURE. Correct exponent was {state['target_exponent']}.", fg=t["danger"], font=("Courier", 13, "bold"))
                    entry_ans.config(state="disabled")
                else:
                    lbl_feedback.config(text=f"ACCESS DENIED. INCORRECT SEQUENCE.", fg=t["danger"])
                    entry_ans.delete(0, tk.END)
                    
        except ValueError:
            play_sfx("error")
            lbl_feedback.config(text="ERR: NUMERIC INPUT REQUIRED", fg=t["danger"])
            entry_ans.delete(0, tk.END)

    def countdown():
        if not state["active"]: return
        
        if state["time_left"] > 0:
            state["time_left"] -= 0.1
            lbl_timer.config(text=f"TIME REMAINING: {state['time_left']:.1f}s")
        else:
            state["lives"] -= 1
            play_sfx("error")
            update_ui()
            
            if state["lives"] <= 0:
                state["active"] = False
                lbl_timer.config(text="TIME REMAINING: 0.0s", fg=t["danger"])
                lbl_header.config(text="MAINFRAME LOCKED", fg=t["danger"])
                lbl_feedback.config(text=f"FAILURE. Correct exponent was {state['target_exponent']}.", fg=t["danger"], font=("Courier", 13, "bold"))
                entry_ans.config(state="disabled")
                return 
            else:
                lbl_feedback.config(text="TIME OUT! LIFE LOST. NEW FIREWALL LOADED.", fg=t["secondary"])
                generate_hack()

        game_win.after(100, countdown)

    entry_ans.bind('<Return>', check_hack)
    generate_hack()
    countdown()

# ==========================================
# 7. BUILD THE SIDEBAR (HISTORY & SETTINGS)
# ==========================================
t = THEMES[current_theme_name]
tk.Label(sidebar, text="CONVERSION\nHISTORY", font=("Arial", 14, "bold"), bg=t["panel"], fg=t["accent"]).pack(pady=10)
listbox_history = tk.Listbox(sidebar, height=14, bg="#222", fg="white", font=("Arial", 10), highlightthickness=0, selectbackground="#333")
listbox_history.pack(padx=10, fill="both", expand=True)

btn_clear = tk.Button(sidebar, text="🗑️ Clear History", command=clear_history, bg="#e94560", fg="white", font=("Arial", 11, "bold"))
btn_clear.pack(pady=10, padx=10, fill="x")

tk.Label(sidebar, text="THEME SELECTOR", font=("Arial", 12, "bold"), bg=t["panel"], fg=t["accent"]).pack(pady=(10, 5))
theme_combo = ttk.Combobox(sidebar, values=list(THEMES.keys()), state="readonly", font=("Arial", 10))
theme_combo.set(current_theme_name)
theme_combo.pack(padx=10, fill="x")
theme_combo.bind("<<ComboboxSelected>>", lambda e: change_theme(theme_combo.get()))

# ==========================================
# 8. BUILD THE MAIN UI IN THE CENTER
# ==========================================
ui_frame = tk.Frame(root, bg=t["panel"], bd=4, relief="ridge")
canvas.create_window(320, 400, window=ui_frame, anchor="center") 

tk.Label(ui_frame, text="🌌 Space-Time Converter 🌌", font=("Arial", 16, "bold"), bg=t["panel"], fg=t["text"]).grid(row=0, column=0, columnspan=3, pady=10)

tk.Label(ui_frame, text="Amount:", bg=t["panel"], fg=t["text"], font=("Arial", 12)).grid(row=1, column=0, pady=5)
entry_value = tk.Entry(ui_frame, font=("Arial", 14), width=12, justify="center")
entry_value.grid(row=1, column=1, columnspan=2, pady=5)

combo_from = ttk.Combobox(ui_frame, values=unit_names, state="readonly", width=16, font=("Arial", 11))
combo_from.set("Kilometer (km)")
combo_from.grid(row=2, column=0, padx=10, pady=10)

btn_swap = tk.Button(ui_frame, text="🔄", command=swap_units, bg="#0f3460", fg="white", font=("Arial", 12))
btn_swap.grid(row=2, column=1)

combo_to = ttk.Combobox(ui_frame, values=unit_names, state="readonly", width=16, font=("Arial", 11))
combo_to.set("Meter (m)")
combo_to.grid(row=2, column=2, padx=10, pady=10)

btn_convert = tk.Button(ui_frame, text="CONVERT", command=do_conversion, bg="#4ade80", fg="black", font=("Arial", 14, "bold"), width=15)
btn_convert.grid(row=3, column=0, columnspan=3, pady=(10, 10))

btn_mission = tk.Button(ui_frame, text="⚠ MISSION: IMPOSSIBLE ⚠", command=launch_mission_impossible, bg="#ff003c", fg="white", font=("Courier", 12, "bold"), width=25)
btn_mission.grid(row=4, column=0, columnspan=3, pady=(0, 20))

tk.Label(ui_frame, text="Standard Number:", bg=t["panel"], fg="gray", font=("Arial", 10)).grid(row=5, column=0, columnspan=3)
lbl_normal_ans = tk.Label(ui_frame, text="0", font=("Courier", 16, "bold"), bg=t["panel"], fg=t["accent"])
lbl_normal_ans.grid(row=6, column=0, columnspan=3)

tk.Label(ui_frame, text="Scientific Notation:", bg=t["panel"], fg="gray", font=("Arial", 10)).grid(row=7, column=0, columnspan=3, pady=(10,0))
lbl_sci_ans = tk.Label(ui_frame, text="0 × 10⁰", font=("Courier", 22, "bold"), bg=t["panel"], fg=t["secondary"])
lbl_sci_ans.grid(row=8, column=0, columnspan=3, pady=(0, 20))

# ==========================================
# 9. KEY BINDINGS & START PROGRAM
# ==========================================
root.bind('<Return>', do_conversion)

def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))
def end_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)

root.mainloop()