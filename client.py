import tkinter as tk
import socket
import cv2
import pickle
import struct
import threading
import sounddevice as sd
import numpy as np

# Function to receive video stream from the server
def receive_video(server_ip):
    global running
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 12345))  # Connect to the server's video port

    data = b""
    payload_size = struct.calcsize("Q")

    while running:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # Receive video packets
            if not packet:
                running = False
                break
            data += packet
        if not running:
            break
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)  # Receive video frame data
        frame_data = data[:msg_size]
        data = data[msg_size:]

        if not frame_data:
            print("Received empty frame data. Skipping.")
            continue

        frame = pickle.loads(frame_data)
        cv2.imshow("Receiving Video", frame)  # Display the video frame
        if cv2.waitKey(1) == 13:  # Break the loop on Enter key press
            break

    client_socket.close()
    cv2.destroyAllWindows()

# Function to receive audio stream from the server
def receive_audio(server_ip):
    global running
    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_socket.connect((server_ip, 12346))  # Connect to the server's audio port

    while running:
        audio_data = audio_socket.recv(1024)  # Receive audio packets
        if not audio_data:
            running = False
            break
        audio_data += b'\0' * (2 - len(audio_data) % 2)
        sd.play(np.frombuffer(audio_data, dtype=np.int16), samplerate=44100, blocking=False)  # Play the received audio data

    audio_socket.close()

# Function to start the video and audio receiving threads
def start_client():
    global video_thread, audio_thread, running
    server_ip = entry.get()  # Get the server IP from the entry widget
    running = True
    video_thread = threading.Thread(target=receive_video, args=(server_ip,))
    audio_thread = threading.Thread(target=receive_audio, args=(server_ip,))
    video_thread.start()  # Start the video thread
    audio_thread.start()  # Start the audio thread

# Function to stop the client
def stop_client():
    global running
    running = False
    root.quit()

# Initialize the Tkinter GUI
root = tk.Tk()
root.title("Client")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Enter the server IP address:")  # Label for the IP entry
label.pack(pady=10)

entry = tk.Entry(frame)  # Entry widget for the server IP
entry.pack(pady=5)

connect_button = tk.Button(frame, text="Connect", command=start_client)  # Button to start the client
connect_button.pack(pady=10)

end_call_button = tk.Button(frame, text="End Call", command=stop_client)  # Button to stop the client
end_call_button.pack(pady=10)

root.mainloop()  # Start the Tkinter event loop
