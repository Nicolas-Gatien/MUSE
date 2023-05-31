import tkinter as tk
import threading
import time
from plyer import notification
from base_command import BaseCommand

class TimerCommand(BaseCommand):
    def __init__(self):
        super().__init__(tag="{TIMER}")

    def execute(self, params=None):
        # if no parameter is passed, default duration is 30 seconds
        duration = int(params) if params is not None else 30
        return f"Timer was started."

        # Create the timer window
        window = tk.Tk()
        window.title('Timer')
        label = tk.Label(window, text='', font=('Helvetica', 24))
        label.pack()

        # Define the countdown function
        def countdown(count):
            # Change text in label
            label['text'] = count

            if count > 0:
                # Call countdown again after 1000ms (1s)
                window.after(1000, countdown, count - 1)
            else:
                window.destroy()
                notification.notify(
                    title='Timer Complete',
                    message='Your timer has finished.',
                    app_icon=None,
                    timeout=10,
                )

        # Start countdown in a separate thread
        countdown_thread = threading.Thread(target=countdown, args=(duration,))
        countdown_thread.start()

        # Start the mainloop in the main thread
        window.mainloop()

        return f"Timer for {duration} seconds has been started."
