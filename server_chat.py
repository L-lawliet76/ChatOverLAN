import tkinter as tk
import socket
import threading

def start_server():
    # Create a socket object for the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12346))  # Bind the socket to all available interfaces on port 12346
    server_socket.listen(5)  # Listen for incoming connections
    print("Chat server started and listening on port 12346")

    # Accept a connection from a client
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established.")

    # Function to receive messages from the client
    def receive_messages():
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:  # Break if no message is received (connection closed)
                break
            chat_box.insert(tk.END, "Client: " + message + "\n")

    # Start a new thread to handle incoming messages
    threading.Thread(target=receive_messages).start()

    # Function to send messages to the client
    def send_message():
        message = message_entry.get()
        chat_box.insert(tk.END, "Server: " + message + "\n")
        client_socket.send(message.encode('utf-8'))
        message_entry.delete(0, tk.END)

    # Initialize the Tkinter GUI
    root = tk.Tk()
    root.title("Chat Server")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(padx=10, pady=10)

    chat_box = tk.Text(frame, height=15, width=50)  # Text widget to display chat messages
    chat_box.pack(pady=10)

    message_entry = tk.Entry(frame, width=40)  # Entry widget to type messages
    message_entry.pack(side=tk.LEFT, padx=5)

    send_button = tk.Button(frame, text="Send", command=send_message)  # Button to send messages
    send_button.pack(side=tk.RIGHT, padx=5)

    root.mainloop()  # Start the Tkinter event loop

    # Close the sockets when the GUI is closed
    client_socket.close()
    server_socket.close()

# Start the server
start_server()
