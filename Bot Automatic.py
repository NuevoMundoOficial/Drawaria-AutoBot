import tkinter as tk
from tkinter import messagebox
import pyautogui
from pynput.keyboard import Key, Listener
import time
import random
import threading
import json

# --- Global Configuration and Stop Flag ---
CONFIG_FILE = "drawaria_bot_config.json"
stop_flag = False
current_status = "Waiting for calibration..."

# --- Keyboard Listener for Emergency Stop ---
def on_press(key):
    global stop_flag
    try:
        if key == Key.esc:
            print("\nESC key pressed. Stopping the bot...")
            stop_flag = True
            return False  # Stop listener
    except AttributeError:
        pass  # Handle special keys that don't have .char

def start_keyboard_listener():
    global current_status
    current_status = "Listening for ESC key..."
    with Listener(on_press=on_press) as listener:
        listener.join()

# --- Bot Logic Class ---
class DrawariaBot:
    def __init__(self, status_callback):
        self.config = self.load_config()
        self.status_callback = status_callback
        self.chat_messages = [
            "hi, what are you doing?",
            "look at what I'm drawing",
            "Xd",
            "almost done",
            "I'm doing something",
            "what a great drawing!",
            "greetings to all",
            "this is fun",
            "who can guess?",
            "focused!"
        ]
        self.drawing_patterns = ['line', 'circle', 'square', 'scribble']
        self.drawing_counter = 0

    def load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)
        self.status_callback("Configuration saved.")

    def update_status(self, message):
        global current_status
        current_status = message
        self.status_callback(message)
        print(f"Status: {message}")

    def calibrate_point(self, point_name):
        self.update_status(f"Move your mouse to the '{point_name}' and press 'c'. Press 'Esc' to cancel.")
        with Listener(on_press=self._on_calibrate_press) as listener:
            self.calibrating = True
            self.calibrated_coord = None
            self.point_name = point_name
            while self.calibrating and not stop_flag:
                time.sleep(0.1)
            if self.calibrated_coord:
                self.config[point_name] = {"x": self.calibrated_coord.x, "y": self.calibrated_coord.y}
                self.save_config()
                self.update_status(f"'{point_name}' calibrated to {self.calibrated_coord}")
            else:
                self.update_status(f"Calibration for '{point_name}' cancelled or failed.")
            self.calibrating = False

    def _on_calibrate_press(self, key):
        try:
            if key.char == 'c':
                self.calibrated_coord = pyautogui.position()
                self.calibrating = False
                return False
            elif key == Key.esc:
                self.calibrating = False
                global stop_flag
                stop_flag = True
                return False
        except AttributeError:
            pass

    def calibrate_color(self, point_name):
        self.update_status(f"Move your mouse to a distinctive pixel for '{point_name}' and press 'c' to capture its coordinates and color. Press 'Esc' to cancel.")
        with Listener(on_press=self._on_color_calibrate_press) as listener:
            self.calibrating = True
            self.calibrated_color_data = None
            self.point_name = point_name
            while self.calibrating and not stop_flag:
                time.sleep(0.1)
            if self.calibrated_color_data:
                self.config[point_name + "_pixel"] = {"x": self.calibrated_color_data["x"], "y": self.calibrated_color_data["y"]}
                self.config[point_name + "_color"] = self.calibrated_color_data["color"]
                self.save_config()
                self.update_status(f"'{point_name}' detection pixel/color calibrated to {self.calibrated_color_data}")
            else:
                self.update_status(f"Calibration for '{point_name}' cancelled or failed.")
            self.calibrating = False

    def _on_color_calibrate_press(self, key):
        try:
            if key.char == 'c':
                pos = pyautogui.position()
                color = pyautogui.screenshot().getpixel((pos.x, pos.y))
                self.calibrated_color_data = {"x": pos.x, "y": pos.y, "color": list(color)}
                self.calibrating = False
                return False
            elif key == Key.esc:
                self.calibrating = False
                global stop_flag
                stop_flag = True
                return False
        except AttributeError:
            pass

    def check_all_calibrated(self):
        required_points = ["playground_button", "canvas_top_left", "canvas_bottom_right", "chat_input_box", "alert_ok_button", "alert_detection_pixel_pixel", "alert_detection_pixel_color"]
        return all(point in self.config for point in required_points)

    def click_point(self, point_name):
        if point_name in self.config:
            x, y = self.config[point_name]["x"], self.config[point_name]["y"]
            pyautogui.moveTo(x, y, duration=random.uniform(0.3, 0.7))
            pyautogui.click()
            self.update_status(f"Clicked {point_name}.")
            time.sleep(random.uniform(0.5, 1.5))
            return True
        else:
            self.update_status(f"Error: {point_name} not calibrated.")
            return False

    def type_message(self, message, chat_input_box_coords):
        pyautogui.moveTo(chat_input_box_coords["x"], chat_input_box_coords["y"], duration=random.uniform(0.2, 0.5))
        pyautogui.click()
        time.sleep(random.uniform(0.1, 0.3))
        pyautogui.typewrite(message, interval=random.uniform(0.05, 0.15))
        pyautogui.press('enter')
        self.update_status(f"Sent message: '{message}'")
        time.sleep(random.uniform(1.0, 3.0))

    def draw_shape(self, canvas_tl, canvas_br):
        if not (canvas_tl and canvas_br):
            self.update_status("Canvas not calibrated for drawing.")
            return

        width = canvas_br["x"] - canvas_tl["x"]
        height = canvas_br["y"] - canvas_tl["y"]

        if width <= 0 or height <= 0:
            self.update_status("Invalid canvas calibration: bottom-right must be greater than top-left.")
            return

        if width < 50 or height < 50:
            self.update_status("Canvas area too small. Please calibrate a larger area.")
            return

        pattern = random.choice(self.drawing_patterns)
        self.update_status(f"Drawing a {pattern}...")

        start_x = random.uniform(canvas_tl["x"], canvas_br["x"])
        start_y = random.uniform(canvas_tl["y"], canvas_br["y"])
        pyautogui.moveTo(start_x, start_y, duration=random.uniform(0.3, 0.7))

        if pattern == 'line':
            end_x = random.uniform(canvas_tl["x"], canvas_br["x"])
            end_y = random.uniform(canvas_tl["y"], canvas_br["y"])
            pyautogui.dragTo(end_x, end_y, duration=random.uniform(0.8, 2.0), button='left')
        elif pattern == 'circle':
            max_radius = min(width, height) / 2 * 0.8
            if max_radius < 10:
                max_radius = 10
            radius = random.uniform(10, max_radius)
            center_x = random.uniform(canvas_tl["x"] + radius, canvas_br["x"] - radius)
            center_y = random.uniform(canvas_tl["y"] + radius, canvas_br["y"] - radius)
            pyautogui.moveTo(center_x + radius, center_y, duration=random.uniform(0.3, 0.7))

            steps = random.randint(30, 60)
            for i in range(steps + 1):
                angle = 2 * 3.1415926535 * (i / steps)
                x = center_x + radius * random.uniform(0.9, 1.1) * (1 - (i/steps * 0.1)) * (angle / (2 * 3.1415926535))
                y = center_y + radius * random.uniform(0.9, 1.1) * (1 - (i/steps * 0.1)) * (angle / (2 * 3.1415926535))
                pyautogui.dragTo(center_x + radius * random.uniform(0.9, 1.1) * (i/steps), center_y + radius * random.uniform(0.9, 1.1) * (i/steps), duration=random.uniform(0.01, 0.05), button='left')
            pyautogui.dragTo(center_x + radius, center_y, duration=random.uniform(0.01, 0.05), button='left')

        elif pattern == 'square':
            side = random.uniform(min(width, height) / 6, min(width, height) / 3)
            top_left_x = random.uniform(canvas_tl["x"], canvas_br["x"] - side)
            top_left_y = random.uniform(canvas_tl["y"], canvas_br["y"] - side)
            pyautogui.moveTo(top_left_x, top_left_y, duration=random.uniform(0.3, 0.7))
            pyautogui.dragTo(top_left_x + side, top_left_y, duration=random.uniform(0.5, 1.0), button='left')
            pyautogui.dragTo(top_left_x + side, top_left_y + side, duration=random.uniform(0.5, 1.0), button='left')
            pyautogui.dragTo(top_left_x, top_left_y + side, duration=random.uniform(0.5, 1.0), button='left')
            pyautogui.dragTo(top_left_x, top_left_y, duration=random.uniform(0.5, 1.0), button='left')

        elif pattern == 'scribble':
            num_points = random.randint(5, 15)
            start_x = random.uniform(canvas_tl["x"], canvas_br["x"])
            start_y = random.uniform(canvas_tl["y"], canvas_br["y"])
            pyautogui.moveTo(start_x, start_y, duration=random.uniform(0.3, 0.7))
            for _ in range(num_points):
                x = random.uniform(canvas_tl["x"], canvas_br["x"])
                y = random.uniform(canvas_tl["y"], canvas_br["y"])
                pyautogui.dragTo(x, y, duration=random.uniform(0.2, 0.8), button='left')

        time.sleep(random.uniform(0.5, 2.5))

    def check_for_alert(self):
        global stop_flag
        if "alert_detection_pixel_pixel" in self.config and "alert_detection_pixel_color" in self.config:
            pixel_x = self.config["alert_detection_pixel_pixel"]["x"]
            pixel_y = self.config["alert_detection_pixel_pixel"]["y"]
            target_color = tuple(self.config["alert_detection_pixel_color"])
            if pyautogui.pixelMatchesColor(pixel_x, pixel_y, target_color, tolerance=15):
                self.update_status("Alert detected! Handling...")
                time.sleep(random.uniform(1.0, 2.0))
                if not self.click_point("alert_ok_button"):
                    self.update_status("Alert OK button not calibrated or click failed. Cannot dismiss alert. Stopping.")
                    stop_flag = True
                    return True
                time.sleep(random.uniform(5.0, 10.0))
                self.update_status("Attempting to re-enter Playground.")
                if not self.click_point("playground_button"):
                    self.update_status("Playground button not calibrated or re-entry failed. Cannot re-enter game. Stopping.")
                    stop_flag = True
                    return True
                self.update_status("Successfully re-entered Playground.")
                return True
        return False

    def main_game_loop(self):
        global stop_flag
        if not self.check_all_calibrated():
            self.update_status("Error: Not all points calibrated. Please calibrate all points first.")
            return

        self.update_status("Starting bot operations...")
        if not self.click_point("playground_button"):
            self.update_status("Failed to enter Playground. Stopping bot.")
            stop_flag = True
            return

        while not stop_flag:
            try:
                if self.check_for_alert():
                    continue

                action_choice = random.choice(['draw', 'chat'])
                if action_choice == 'draw':
                    self.draw_shape(self.config.get("canvas_top_left"), self.config.get("canvas_bottom_right"))
                    self.drawing_counter += 1
                    if random.random() < 0.3 or self.drawing_counter % random.randint(3, 7) == 0:
                        self.type_message(random.choice(self.chat_messages), self.config.get("chat_input_box"))
                else:
                    self.type_message(random.choice(self.chat_messages), self.config.get("chat_input_box"))
                    time.sleep(random.uniform(1.0, 3.0))

                time.sleep(random.uniform(0.5, 2.0))

                if stop_flag:
                    break
            except pyautogui.FailSafeException:
                self.update_status("PyAutoGUI FailSafe triggered (mouse moved to corner). Stopping bot.")
                stop_flag = True
                break
            except Exception as e:
                self.update_status(f"An unexpected error occurred: {e}. Stopping bot.")
                stop_flag = True
                break

        self.update_status("Bot stopped.")

# --- Tkinter GUI ---
class DrawariaApp:
    def __init__(self, master):
        self.master = master
        master.title("Drawaria.online Autobot")
        master.geometry("400x550")
        self.bot = DrawariaBot(self.update_status_label)
        self.status_label = tk.Label(master, text=current_status, wraplength=380, fg="blue")
        self.status_label.pack(pady=10)
        self.calibrate_labels = {}

        calibration_points = {
            "playground_button": "Playground Button (e.g., 'Play' or 'Join Playground')",
            "canvas_top_left": "Canvas Top-Left Corner (for drawing area)",
            "canvas_bottom_right": "Canvas Bottom-Right Corner (for drawing area)",
            "chat_input_box": "Chat Input Box (where you type messages)",
            "alert_ok_button": "Alert 'OK' Button (e.g., disconnect/reload alerts)",
            "alert_detection_pixel": "Alert Detection Pixel (a pixel that changes color ONLY when an alert appears)"
        }

        for key, text in calibration_points.items():
            frame = tk.Frame(master)
            frame.pack(pady=2, fill='x', padx=10)
            label_text = tk.Label(frame, text=f"{text}:", anchor='w')
            label_text.pack(side='left', padx=(0, 5))
            coord_label = tk.Label(frame, text="N/A", anchor='w')
            coord_label.pack(side='left', expand=True, fill='x')
            self.calibrate_labels[key] = coord_label
            btn = tk.Button(frame, text="Calibrate", command=lambda k=key: self.start_calibration(k))
            btn.pack(side='right')

        self.start_button = tk.Button(master, text="START AUTOBOT", command=self.start_bot)
        self.start_button.pack(pady=20)
        self.check_calibration_status()

    def update_status_label(self, message):
        self.status_label.config(text=message)

    def check_calibration_status(self):
        for key, label_widget in self.calibrate_labels.items():
            if key == "alert_detection_pixel":
                pixel_coords = self.bot.config.get(key + "_pixel", {})
                pixel_color = self.bot.config.get(key + "_color", "N/A")
                coord_str = f"X: {pixel_coords.get('x', 'N/A')}, Y: {pixel_coords.get('y', 'N/A')}, Color: {pixel_color}"
            else:
                current_coords = self.bot.config.get(key, {})
                coord_str = f"X: {current_coords.get('x', 'N/A')}, Y: {current_coords.get('y', 'N/A')}"
            label_widget.config(text=coord_str)

        if self.bot.check_all_calibrated():
            self.update_status_label("All points calibrated! Ready to start.")
            self.start_button.config(state=tk.NORMAL)
        else:
            self.update_status_label("Please calibrate all points before starting.")
            self.start_button.config(state=tk.DISABLED)

    def start_calibration(self, point_name):
        self.start_button.config(state=tk.DISABLED)
        for btn_key in self.calibrate_labels:
            self.calibrate_labels[btn_key].master.winfo_children()[-1].config(state=tk.DISABLED)

        def calibrate_thread():
            if point_name == "alert_detection_pixel":
                self.bot.calibrate_color(point_name)
            else:
                self.bot.calibrate_point(point_name)

            self.master.after(100, self.check_calibration_status)
            for btn_key in self.calibrate_labels:
                self.calibrate_labels[btn_key].master.winfo_children()[-1].config(state=tk.NORMAL)

        threading.Thread(target=calibrate_thread).start()

    def start_bot(self):
        global stop_flag
        stop_flag = False

        if not self.bot.check_all_calibrated():
            messagebox.showerror("Error", "Please calibrate all required points before starting the bot.")
            return
        self.start_button.config(state=tk.DISABLED, text="BOT RUNNING (Press ESC to Stop)")

        keyboard_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
        keyboard_thread.start()

        bot_thread = threading.Thread(target=self.bot.main_game_loop, daemon=True)
        bot_thread.start()

        self.master.after(100, self.monitor_bot_status)

    def monitor_bot_status(self):
        if stop_flag:
            self.start_button.config(state=tk.NORMAL, text="START AUTOBOT")
            self.update_status_label("Bot gracefully stopped.")
            messagebox.showinfo("Bot Status", "The Drawaria.online bot has stopped.")
        else:
            self.status_label.config(text=current_status)
            self.master.after(100, self.monitor_bot_status)

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawariaApp(root)
    root.mainloop()
