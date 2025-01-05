import socket
import tkinter as tk
from random import randint
import threading
from tkinter import messagebox
import struct
from PIL import Image, ImageTk
import io
import time

# Adjust this to your system's screen resolution or the client's resolution if you know it
client_screen_width = 1366  # Example client screen width
client_screen_height = 768  # Example client screen height

last_motion_time = 0

def receive_video(conn, label, root):
    """Receive video frames from the client and display them."""
    while True:
        try:
            # Receive the size of the incoming frame
            packet = conn.recv(8)
            if not packet:
                break
            frame_size = struct.unpack("Q", packet)[0]

            # Receive the actual frame data
            data = b""
            while len(data) < frame_size:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet

            # Convert the received data to an image
            image = Image.open(io.BytesIO(data))  

            # Resize the image to match the server's window size (client screen size)
            current_width, current_height = root.winfo_width(), root.winfo_height()
            img = image.resize((current_width, current_height))

            # Convert the PIL Image to a Tkinter PhotoImage
            img_tk = ImageTk.PhotoImage(img)

          
            root.after(1, lambda: label.config(image=img_tk))
            label.image = img_tk  # Prevent garbage collection

        except Exception as e:
            print(f"Video streaming error: {e}")
            break

def control_client(cursor_data, conn):
    """Send control commands to the client."""
    try:
        conn.sendall(cursor_data.encode())
    except Exception as e:
        print(f"Error sending control command: {e}")

def type_box(conn):
    """Function for the 'Type' menu item."""
    tp_fr = tk.Toplevel()
    tp_fr.title('Python Remote Keyboard')
    bx_txt = tk.Entry(tp_fr, width=100)
    bx_txt.pack()
    send_but = tk.Button(tp_fr, text="Type Text", command=lambda: conn.send(('cde:' + bx_txt.get()).encode()))
    del_but = tk.Button(tp_fr, text="Delete", command=lambda: conn.send('del'.encode()))
    nl_but = tk.Button(tp_fr, text="Enter", command=lambda: conn.send('nl'.encode()))
    del_but.pack()
    send_but.pack()
    nl_but.pack()

# Main Code
port = randint(1000, 10000)
host = socket.gethostname()
ip = socket.gethostbyname(host)

info_root = tk.Tk()
info_root.withdraw()  # Hide the main window
tk.messagebox.showinfo('Control Data', f'Host = {ip}\nPort = {port}')
info_root.destroy()

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(2)
print("Waiting for a connection...")
conn, address = server_socket.accept()
print("Connection from: " + str(address))

# Main Application Window
root = tk.Tk()
root.title('Python Remote Control')
root.geometry('960x720')  

video_label = tk.Label(root)
video_label.pack()

def motion(event):
    global last_motion_time
    current_time = time.time()

    if current_time - last_motion_time > 0.01:  
        x, y = event.x, event.y
        cursor_data = f"{x * 2} {y * 2}"
        control_client(cursor_data, conn)
        last_motion_time = current_time

root.bind('<Motion>', motion)

def left_click(event):
    control_client('c', conn)

def right_click(event):
    control_client('r', conn)

def double_click(event):
    control_client('d', conn)

root.bind('<Button-1>', left_click)
root.bind('<Button-3>', right_click)
root.bind('<Double-Button-1>', double_click)

menu = tk.Menu(root)
menu.add_command(label="Type", command=lambda: type_box(conn))
root.config(menu=menu)

# Start the video thread
video_thread = threading.Thread(target=receive_video, args=(conn, video_label, root))
video_thread.daemon = True
video_thread.start()

root.mainloop()
