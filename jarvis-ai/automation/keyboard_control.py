import pyautogui
import time
import keyboard as kb  # using the 'keyboard' pip module if needed for hotkeys, but pyautogui does most well

class KeyboardController:
    def type_text(self, text: str, interval: float = 0.05):
        """Simulates human typing for the string provided."""
        pyautogui.write(text, interval=interval)

    def press_key(self, key_name: str):
        """Presses and releases a single key (e.g., 'enter', 'esc', 'tab')."""
        pyautogui.press(key_name)

    def hotkey(self, *keys):
        """Executes a key combination (e.g. hotkey('ctrl', 'c'))."""
        pyautogui.hotkey(*keys)

    def hold_key(self, key_name: str, duration: float):
        """Holds a key down for a specified duration."""
        pyautogui.keyDown(key_name)
        time.sleep(duration)
        pyautogui.keyUp(key_name)

keyboard = KeyboardController()
