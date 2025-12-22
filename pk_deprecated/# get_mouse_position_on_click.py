import logging
from pynput import mouse
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

def get_mouse_position_on_click() -> Point:
    """
    Waits for a single left mouse click and returns its coordinates.

    Returns:
        Point: A dataclass object with x and y attributes for the click position.
    """
    click_position = None
    
    def on_click(x, y, button, pressed):
        nonlocal click_position
        # We only care about the press event of the left button
        if pressed and button == mouse.Button.left:
            click_position = Point(x=int(x), y=int(y))
            # Stop the listener
            return False

    # Collect events until the listener is stopped
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
        
    if click_position:
        logging.debug(f"Mouse clicked at: {click_position.x}, {click_position.y}")
    
    return click_position
