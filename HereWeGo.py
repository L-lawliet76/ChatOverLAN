import tkinter as tk
from tkinter import messagebox
import subprocess
import socket

# Function to start the video server by running 'server.py'
def start_server_video():
    subprocess.Popen(['python', 'server.py'])
    root.destroy()  # Close the current Tkinter window

# Function to start the video client by running 'client.py'
def start_client_video():
    subprocess.Popen(['python', 'client.py'])
    root.destroy()  # Close the current Tkinter window

# Function to start the chat server
def start_server_chat():
    for widget in frame.winfo_children():  # Remove all widgets from the frame
        widget.destroy()

    display_ip()  # Display the server IP address

    label = tk.Label(frame, text="Waiting for connection...")
    label.pack(pady=10)

    subprocess.Popen(['python', 'server_chat.py'])
    root.destroy()  # Close the current Tkinter window

# Function to start the chat client
def start_client_chat():
    for widget in frame.winfo_children():  # Remove all widgets from the frame
        widget.destroy()

    label = tk.Label(frame, text="Enter the server IP address:")
    label.pack(pady=10)

    ip_entry = tk.Entry(frame)  # Entry widget for the user to input server IP address
    ip_entry.pack(pady=5)

    connect_button = tk.Button(frame, text="Connect", command=lambda: connect_chat(ip_entry.get()))
    connect_button.pack(pady=10)

# Function to connect to the chat server with the provided IP address
def connect_chat(ip_address):
    subprocess.Popen(['python', 'client_chat.py', ip_address])
    root.destroy()  # Close the current Tkinter window

# Function to display the IP address of the host machine
def display_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    ip_label = tk.Label(frame, text=f"Your IP Address: {ip_address}")
    ip_label.pack(pady=10)

# Function to handle user choice between video call and chat
def choose_option(option):
    for widget in frame.winfo_children():  # Remove all widgets from the frame
        widget.destroy()

    if option == "video":
        label = tk.Label(frame, text="Do you want to call someone or receive a call?")
        label.pack(pady=10)

        call_button = tk.Button(frame, text="Call Someone", command=start_client_video)
        call_button.pack(side=tk.LEFT, padx=10)

        receive_button = tk.Button(frame, text="Receive a Call", command=start_server_video)
        receive_button.pack(side=tk.RIGHT, padx=10)

    elif option == "chat":
        label = tk.Label(frame, text="Do you want to start a chat or receive a chat?")
        label.pack(pady=10)

        start_chat_button = tk.Button(frame, text="Start Chat", command=start_client_chat)
        start_chat_button.pack(side=tk.LEFT, padx=10)

        receive_chat_button = tk.Button(frame, text="Receive Chat", command=start_server_chat)
        receive_chat_button.pack(side=tk.RIGHT, padx=10)

# Initialize the main Tkinter window
root = tk.Tk()
root.title("LAN Communication")

# Create a frame to hold widgets with padding
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

# Initial label asking the user to choose between video call and chat
label = tk.Label(frame, text="Do you want to video call or chat?")
label.pack(pady=10)

# Buttons for video call and chat options
video_button = tk.Button(frame, text="Video Call", command=lambda: choose_option("video"))
video_button.pack(side=tk.LEFT, padx=10)

chat_button = tk.Button(frame, text="Chat", command=lambda: choose_option("chat"))
chat_button.pack(side=tk.RIGHT, padx=10)

# Start the Tkinter main event loop
root.mainloop()
