import tkinter as tk
import socket
from threading import Thread
import cv2
import pickle
import struct
import threading
import sounddevice as sd
import numpy as np

# Function to send audio data to the client
def send_audio(client_socket):
    while True:
        # Record audio data
        audio_data = sd.rec(1024, samplerate=44100, channels=2, dtype=np.int16)
        client_socket.sendall(audio_data.tobytes())  # Send audio data to the client

# Function to get the IP address of the server
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

# Function to start the server
def start_server():
    global running
    # Create and bind video server socket
    video_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    video_server_socket.bind(('0.0.0.0', 12345))
    video_server_socket.listen(5)
    print("Video server started and listening on port 12345")

    # Create and bind audio server socket
    audio_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_server_socket.bind(('0.0.0.0', 12346))
    audio_server_socket.listen(5)
    print("Audio server started and listening on port 12346")

    # Accept video connection
    video_client_socket, address = video_server_socket.accept()
    print(f"Video connection from {address} has been established.")

    # Accept audio connection
    audio_client_socket, address = audio_server_socket.accept()
    print(f"Audio connection from {address} has been established.")

    # Start audio sending thread
    audio_thread = Thread(target=send_audio, args=(audio_client_socket,))
    audio_thread.start()

    try:
        cap = cv2.VideoCapture(0)  # Open webcam for video capture
    except cv2.error as e:
        print(f"Error opening webcam: {e}")
        cap = None

    # Loop to send video frames to the client
    while running and (cap is None or cap.isOpened()):
        if cap is not None:
            ret, frame = cap.read()  # Capture a video frame
            if not ret:
                break
            data = pickle.dumps(frame)  # Serialize the frame
        else:
            # If webcam is not available, send a placeholder frame
            data = pickle.dumps("NO_WEBCAM")

        message = struct.pack("Q", len(data)) + data  # Pack the message with the size of the data
        video_client_socket.sendall(message)  # Send the message to the client

    if cap is not None:
        cap.release()  # Release the webcam
    video_client_socket.close()  # Close the video client socket
    audio_client_socket.close()  # Close the audio client socket
    video_server_socket.close()  # Close the video server socket
    audio_server_socket.close()  # Close the audio server socket

# Function to run the server in a separate thread
def run_server():
    global server_thread, running
    running = True
    server_thread = Thread(target=start_server)
    server_thread.start()

# Function to stop the server
def stop_server():
    global running
    running = False
    root.quit()

# Function to display the server's IP address
def show_ip_address():
    ip_address = get_ip_address()
    ip_label.config(text=f"Your IP Address: {ip_address}")

# Initialize the Tkinter GUI
root = tk.Tk()
root.title("Server")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Server is running. Waiting for connections...")  # Label to indicate server status
label.pack(pady=10)

ip_label = tk.Label(frame, text="")  # Label to display the IP address
ip_label.pack(pady=10)

show_ip_button = tk.Button(frame, text="Show IP Address", command=show_ip_address)  # Button to show IP address
show_ip_button.pack(pady=10)

end_call_button = tk.Button(frame, text="End Call", command=stop_server)  # Button to end the call
end_call_button.pack(pady=10)

run_server()  # Start the server

root.mainloop()  # Start the Tkinter event loop
