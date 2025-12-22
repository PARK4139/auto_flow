import tkinter as tk
import logging

class ROISelector:
    """
    A draggable, resizable, semi-transparent window to visually select a Region of Interest (ROI).
    """
    def __init__(self, key_name: str, title="Drag and resize to select ROI"):
        self.root = tk.Tk()
        self.root.title(title)
        self.key_name = key_name
        
        # Initial geometry
        self.root.geometry('300x200+100+100')
        
        # Make window semi-transparent and borderless
        self.root.attributes('-alpha', 0.5)
        self.root.overrideredirect(True)
        
        # Make window stay on top
        self.root.attributes('-topmost', True)

        self.roi_coords = None

        # --- WIDGETS ---
        # Main frame
        self.main_frame = tk.Frame(self.root, bg='sky blue')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label (for instructions)
        self.title_label = tk.Label(self.main_frame, text=title, bg='sky blue', fg='black')
        self.title_label.pack(pady=2, side=tk.TOP)

        # Coordinates display label
        self.coords_label = tk.Label(self.main_frame, text="", bg='sky blue', fg='black', font=("Arial", 10))
        self.coords_label.pack(pady=2, side=tk.TOP)

        # KeyName Label (to display the key_name prominently)
        font_size = 12 # Reduced from 16
        self.key_name_label = tk.Label(self.main_frame, text=self.key_name, bg='sky blue', fg='black', font=("Arial", font_size, "bold"))
        self.key_name_label.pack(pady=10, expand=True)

        # Buttons frame
        self.buttons_frame = tk.Frame(self.main_frame, bg='sky blue')
        self.buttons_frame.pack(side=tk.BOTTOM, pady=10)
        
        # Set ROI Button
        self.set_button = tk.Button(self.buttons_frame, text="Set ROI", command=self.on_set)
        self.set_button.pack(side=tk.LEFT, padx=10)
        
        # Cancel Button
        self.cancel_button = tk.Button(self.buttons_frame, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

        # Resize Grip
        self.grip = tk.Label(self.main_frame, bg='blue')
        self.grip.place(relx=1.0, rely=1.0, anchor='se', width=10, height=10)

        # --- BINDINGS ---
        # Bindings for dragging the window
        draggable_widgets = [self.main_frame, self.title_label, self.key_name_label, self.coords_label]
        for widget in draggable_widgets:
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<ButtonRelease-1>", self.stop_move)
            widget.bind("<B1-Motion>", self.do_move)

        # Bindings for resizing the window
        self.grip.bind("<ButtonPress-1>", self.start_resize)
        self.grip.bind("<ButtonRelease-1>", self.stop_resize)
        self.grip.bind("<B1-Motion>", self.do_resize)

        # Variables to store drag/resize start positions
        self._drag_start_x = 0
        self._drag_start_y = 0
        
        # Call once to set initial coordinates display
        self.root.update_idletasks() # Ensure window info is available
        self._update_coords_display()


    def _update_coords_display(self):
        """Updates the coordinate label with the window's current position and size."""
        x1 = self.root.winfo_x()
        y1 = self.root.winfo_y()
        x2 = x1 + self.root.winfo_width()
        y2 = y1 + self.root.winfo_height()
        self.coords_label.config(text=f"({x1}, {y1}) - ({x2}, {y2})")

    def start_move(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def stop_move(self, event):
        self._drag_start_x = None
        self._drag_start_y = None

    def do_move(self, event):
        dx = event.x - self._drag_start_x
        dy = event.y - self._drag_start_y
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")
        self._update_coords_display()

    def start_resize(self, event):
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    def stop_resize(self, event):
        self._drag_start_x = None
        self._drag_start_y = None

    def do_resize(self, event):
        dx = event.x_root - self._drag_start_x
        dy = event.y_root - self._drag_start_y
        new_width = self.root.winfo_width() + dx
        new_height = self.root.winfo_height() + dy
        self.root.geometry(f"{new_width}x{new_height}")
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root
        self._update_coords_display()

    def on_set(self):
        """
        Callback for the 'Set ROI' button. Stores the final coordinates and closes the window.
        """
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.roi_coords = {
            "x1": x,
            "y1": y,
            "x2": x + width,
            "y2": y + height
        }
        logging.info(f"ROI selected: {self.roi_coords}")
        self.root.quit()

    def on_cancel(self):
        """
        Callback for the 'Cancel' button. Closes the window without saving.
        """
        self.roi_coords = None
        logging.info("ROI selection cancelled.")
        self.root.quit()

    def run(self) -> dict | None:
        """
        Shows the window and starts the main loop.

        Returns:
            dict | None: The selected ROI coordinates or None if cancelled.
        """
        self.root.mainloop()
        # After mainloop is quit, destroy the window
        self.root.destroy()
        return self.roi_coords

if __name__ == '__main__':
    # Example usage for testing
    logging.basicConfig(level=logging.INFO)
    print("Showing ROI selector. Close the window or click a button to finish.")
    selector = ROISelector(key_name="Test ROI", title="Select an area and click 'Set ROI'")
    selected_area = selector.run()

    if selected_area:
        print(f"Final selected area: {selected_area}")
    else:
        print("Selection was cancelled.")
