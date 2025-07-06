Drawaria.online Autobot - README
Welcome to the Drawaria.online Autobot!

This script is designed to automate actions within the Drawaria.online game, specifically focusing on drawing shapes and sending chat messages. It uses pyautogui for mouse and keyboard control, and pynput for listening to the ESC key for an emergency stop.

Please read this guide carefully before using the bot.

Features:

Automated Drawing: Draws random shapes (lines, circles, squares, scribbles) within a calibrated drawing area.

Automated Chat: Sends random chat messages from a predefined list.

Calibration System: Guides you through calibrating essential game elements like buttons, the drawing canvas, and chat input.

Alert Detection: Can detect and dismiss common in-game alerts (e.g., disconnection, reload) by monitoring a specific pixel's color.

Emergency Stop: Press the ESC key at any time to immediately stop the bot's operations.

Configuration Persistence: Saves calibration data to drawaria_bot_config.json so you don't have to recalibrate every time.

Requirements:

Python 3: Ensure you have Python 3 installed on your system.

Libraries: You'll need to install the following Python libraries:

Generated bash
pip install pyautogui pynput

How to Use:
1. Calibration is Crucial!

Before you can start the bot, you must calibrate all the required points in the Drawaria.online game. The bot needs to know where specific elements are on your screen.

Launch Drawaria.online: Open Drawaria.online in your web browser.

Open the Autobot GUI: Run the Python script (python your_script_name.py). A GUI window will appear.

Calibrate Each Element:

Click the "Calibrate" button next to each item in the GUI.

The GUI will tell you what to do. Typically, you'll need to move your mouse cursor to the correct location in the Drawaria.online game.

Press 'c' on your keyboard when your mouse is in the correct position.

For "Alert Detection Pixel": Move your mouse to a pixel that only changes its color when an alert appears (e.g., a specific part of the alert box's background). Then press 'c'. The bot will capture both the pixel's coordinates and its current color.

Press 'ESC' to cancel a calibration if you make a mistake.

After each successful calibration, the GUI will update with the coordinates.

The required calibration points are:

Playground Button: The button you click to join or start a new game (e.g., "Play", "Join Playground").

Canvas Top-Left Corner: The top-left corner of the main drawing area in the game.

Canvas Bottom-Right Corner: The bottom-right corner of the main drawing area.

Chat Input Box: The text field where you type messages.

Alert 'OK' Button: The button you click to dismiss alerts (like disconnect messages).

Alert Detection Pixel: A specific pixel that changes color only when an alert is active. (This requires calibrating both the pixel coordinates and its color).

2. Starting the Autobot:

Once all points are calibrated, the "START AUTOBOT" button will become enabled.

Click "START AUTOBOT".

The bot will begin its automated process of drawing and chatting.

3. Stopping the Autobot:

To stop the bot at any time, simply press the ESC key on your keyboard.

The bot will gracefully shut down, and a message will appear in the GUI.

Configuration:

When you calibrate points, their coordinates are saved to a file named drawaria_bot_config.json in the same directory as the script.

You can edit this file manually if you know what you're doing, but it's recommended to use the in-script calibration process.

Important Notes:

Screen Resolution/Layout: The bot relies on fixed coordinates. If you change your screen resolution, zoom levels, or the game's layout, you will need to recalibrate.

Game Updates: If Drawaria.online is updated and the game elements move or change appearance, you will need to recalibrate.

Be Respectful: Use this bot responsibly and avoid spamming or disrupting other players' experiences.

No Guarantees: This bot is provided as-is. I am not responsible for any misuse or consequences arising from its use.

False Positives: The alert detection relies on color matching. Ensure you select a pixel that is truly unique to the alert state. A small tolerance is used, but in some cases, it might trigger incorrectly or fail to trigger.

First Run: On the first run, the bot will likely prompt you to calibrate everything.

Troubleshooting:

Bot not starting: Make sure all calibration points are set (check the GUI for "N/A" values).

Bot clicking the wrong thing: Double-check your calibrations. Recalibrate the specific point that seems off.

Bot not stopping: If the ESC key doesn't work, you may need to force-quit the Python script from your operating system's task manager.

Enjoy using the Drawaria.online Autobot!
