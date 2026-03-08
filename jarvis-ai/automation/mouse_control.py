import pyautogui

class MouseController:
    def __init__(self):
        # Configure fail-safe (moving mouse to corner stops it)
        pyautogui.FAILSAFE = True
        
    def get_position(self):
        """Returns the current mouse X and Y coordinates."""
        return pyautogui.position()

    def move_to(self, x: int, y: int, duration: float = 0.5):
        """Moves the mouse to the absolute coordinates over the specified duration."""
        pyautogui.moveTo(x, y, duration=duration)

    def click(self, x: int = None, y: int = None, button: str = 'left'):
        """Clicks the button at current position, or at (x, y) if provided."""
        if x is not None and y is not None:
            pyautogui.click(x=x, y=y, button=button)
        else:
            pyautogui.click(button=button)

    def double_click(self, x: int = None, y: int = None):
        """Double clicks left mouse button."""
        if x is not None and y is not None:
            pyautogui.doubleClick(x=x, y=y)
        else:
            pyautogui.doubleClick()

    def scroll(self, amount: int):
        """Scrolls the mouse wheel up (positive) or down (negative)."""
        pyautogui.scroll(amount)

mouse = MouseController()
