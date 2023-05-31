import tkinter as tk
import threading
import time
from plyer import notification

duration = 30

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

        # Use threading to prevent blocking
threading.Thread(target=countdown, args=(duration,)).start()

window.mainloop()