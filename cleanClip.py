"""
README for Whitespace Removal Script

Description:
This script is designed to automatically remove leading whitespace from text copied to the clipboard. It is particularly useful when working with large language models (LLMs) like ChatGPT, as it reduces the number of tokens used by eliminating unnecessary spaces. The script listens for specific keyboard commands and then cleans the clipboard contents, removing leading whitespaces from each line.

Usage:
1. Run the script in your Python environment.
2. Copy any text with leading whitespace to your clipboard.
3. Press 'Command + Shift + V' on your keyboard.
4. The script will automatically clean the clipboard by removing leading whitespaces and then simulate a paste action.

Irony and Limitations:
- This script is written in Python, a language that relies on indentation for its syntax. Ironically, it cannot be used to process Python code, as removing leading whitespace could alter the code's functionality.
- The script doesn't change the original formatting of documents or code in other applications; it only alters the text in the clipboard.

Security and Permissions:
- The script monitors keyboard inputs to trigger its functionality, which may raise security concerns regarding keylogging. Users should review the script to ensure it aligns with their security standards.
- Special permissions might be required to allow the script to control the keyboard and access the clipboard. Users must grant these permissions for the script to function correctly.

Dependencies:
- pyperclip: Used for accessing and modifying the clipboard.
- pynput: Utilized for monitoring keyboard inputs and simulating key presses.

Note: Always ensure that granting such permissions aligns with your security protocols and system guidelines.
"""


import pyperclip
import logging
from pynput import keyboard
from pynput.keyboard import Key, Controller

logging.basicConfig(level=logging.INFO)

keyboard_controller = Controller()

def remove_whitespace(text):
    if text is None:
        return text
    lines = text.split('\n')
    processed_lines = [line.lstrip() for line in lines]
    return '\n'.join(processed_lines)

def clean_clipboard():
    current_clipboard = pyperclip.paste()
    logging.info(f"Current Clipboard: {current_clipboard}")
    if current_clipboard:
        cleaned_text = remove_whitespace(current_clipboard)
        pyperclip.copy(cleaned_text)
        logging.info(f"Cleaned Clipboard: {cleaned_text}")
        simulate_paste()

def simulate_paste():
    keyboard_controller.press(Key.cmd)
    keyboard_controller.press('v')
    keyboard_controller.release('v')
    keyboard_controller.release(Key.cmd)

pressed_keys = set()

def on_press(key):
    pressed_keys.add(key)
    if Key.cmd in pressed_keys and key == keyboard.KeyCode.from_char('v'):
        if Key.shift in pressed_keys:
            clean_clipboard()

def on_release(key):
    pressed_keys.discard(key)
    if key == Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
