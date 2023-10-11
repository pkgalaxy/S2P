import tkinter as tk
import os
from PIL import ImageGrab, Image
import threading
import keyboard
import time
import tqdm

# Set the screenshot and PDF folder paths
desktop_folder = os.path.join(os.path.expanduser('~'), 'Desktop')
screenshot_folder = os.path.join(desktop_folder, 'screenshot_folder')
pdf_folder = os.path.join(desktop_folder, 'pdfs_folder')

# Create screenshot and PDF folders if they don't exist
os.makedirs(screenshot_folder, exist_ok=True)
os.makedirs(pdf_folder, exist_ok=True)

# Read the current screenshot count from a file or initialize to 1 if the file doesn't exist
screenshot_count_file = os.path.join(os.path.expanduser('~'), 'screenshot_count.txt')
if os.path.exists(screenshot_count_file):
    with open(screenshot_count_file, 'r') as f:
        screenshot_count = int(f.read())
else:
    screenshot_count = 1

def update_screenshot_count():
    with open(screenshot_count_file, 'w') as f:
        f.write(str(screenshot_count))

def flash_screen(duration=0.2):
    flash_window = tk.Tk()
    flash_window.attributes('-fullscreen', True)
    flash_window.configure(bg='white')
    flash_window.update()
    time.sleep(duration)
    flash_window.destroy()

def take_screenshot():
    os.makedirs(screenshot_folder, exist_ok=True)
    global screenshot_count
    screenshot = ImageGrab.grab()
    screenshot_path = os.path.join(screenshot_folder, f'screenshot_{screenshot_count}.png')
    try:
        screenshot.save(screenshot_path, 'PNG')  # Save as PNG format
        screenshot_count += 1
        flash_screen()
        time.sleep(0.5)
        update_screenshot_count()  # Update the screenshot count in the file
    except Exception as e:
        print(f"Error saving screenshot: {e}")

# ... (the rest of your code remains the same)



def remove_ss():
    try:
        # List all files in the screenshot folder
        screenshot_files = os.listdir(screenshot_folder)

        # Iterate through the files and remove them
        for file_name in screenshot_files:
            file_path = os.path.join(screenshot_folder, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All screenshots removed successfully.")
    except Exception as e:
        print(f"Error removing screenshots: {e}")

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image

def create_pdf():
    try:
        # Initialize the PDF document
        os.makedirs(pdf_folder, exist_ok=True)
        timestamp = time.strftime("%Y%m%d%H%M%S")
        pdf_path = os.path.join(pdf_folder, f'screenshots_{timestamp}.pdf')
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)

        elements = []
        screenshot_files = os.listdir(screenshot_folder)
        screenshot_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
        # progress_bar = tqdm(total=len(screenshot_files), desc="Creating PDF")
        # Iterate through all screenshot files and add them to the PDF as images without scaling
        for file_name in screenshot_files:
            screenshot_path = os.path.join(screenshot_folder, file_name)
            try:
                img = Image(screenshot_path)
                img.drawHeight = 720  # Set the height of the image
                img.drawWidth = 1280   # Set the width of the image
                elements.append(img)
                # progress_bar.update(1)
            except Exception as e:
                print(f"Error adding screenshot {file_name} to PDF: {e}")

        # Build and save the PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=(1720, 880))  # Adjust the page size as needed
        doc.build(elements)
        # progress_bar.close()
        print(f"PDF '{pdf_path}' created successfully.")
    except Exception as e:
        print(f"Error creating PDF: {e}")


# Function to listen for the "/" key press using the keyboard library
def listen_for_screenshot_key():
    while True:
        keyboard.wait("`")  # Wait for the "`" key press
        take_screenshot()

################# WINDOW ###################
root = tk.Tk()
root.geometry("400x290")
root.iconbitmap("icon.ico")
# root.configure(bg="black")
root.title("Screenshot to PDF")
root.minsize(400, 290)
root.maxsize(400, 290)
tk.Label(root, text="Screenshot to PDF generator", font="arial 18 bold"  ,fg="dark red", bg="grey").pack(fill=tk.X)
tk.Label(root, text="Automatic", font="arial 12 bold"  ,fg="dark red", bg="grey").pack(fill=tk.X)

tk.Label(root, text="For taking screenshot press:  ` ", font="bold").pack(pady=10)


def on_hover_hand(event):
    event.widget.config(cursor="hand2")
    
def on_leave_default(event):
    event.widget.config(cursor="hand2")
    
button_1 = tk.Button(root, text="Create PDF",bg="Green",fg="White" , command=create_pdf)
button_1.pack(padx=10, pady=20)
button_2 = tk.Button(root, text="Remove All screenshots",bg="Red",fg="White" , command=remove_ss)
button_2.pack(padx=10, pady=40)

button_1.bind("<Enter>", on_hover_hand)
button_2.bind("<Leave>", on_leave_default)

# Create separate threads to listen for the "/" and "+" key presses
screenshot_thread = threading.Thread(target=listen_for_screenshot_key)
screenshot_thread.daemon = True
screenshot_thread.start()

root.mainloop()
