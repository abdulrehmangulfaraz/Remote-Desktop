import socket
import threading
import struct
import pyautogui
from PIL import ImageGrab
import io

pyautogui.FAILSAFE = False

def send_screen(server_socket):
    """Capture and send screen content to the server."""
    try:
        while True:
            # Capture the screen
            screen = ImageGrab.grab()
            
            
            # Convert the image to bytes
            byte_io = io.BytesIO()
            screen.save(byte_io, format='PNG')
            byte_data = byte_io.getvalue()

            # Send the size of the frame followed by the frame data
            frame_size = struct.pack("Q", len(byte_data))
            server_socket.sendall(frame_size)
            server_socket.sendall(byte_data)

    except Exception as e:
        print(f"Screen sharing error: {e}")

def receive_commands(server_socket):
    """Receive and execute control commands from the server."""
    try:
        while True:
            command = server_socket.recv(1024).decode()
            if not command:
                break

            if command.startswith('cde:'):
                pyautogui.typewrite(command[4:])
            elif command == 'del':
                pyautogui.press('backspace')
            elif command == 'nl':
                pyautogui.press('enter')
            elif command == 'c':
                pyautogui.click()
            elif command == 'r':
                pyautogui.rightClick()
            elif command == 'd':
                pyautogui.doubleClick()
            else:
                try:
                    # Handle cursor data (x, y)
                    x, y = map(int, command.split())
                    pyautogui.moveTo(x, y)
                except ValueError:
                    print(f"Invalid cursor data: {command}")
    except Exception as e:
        print(f"Command receiving error: {e}")

if 1:
    try:
        server_ip = input("Enter the server IP address: ")
        server_port = int(input("Enter the server port: "))

        client_socket = socket.socket()
        client_socket.connect((server_ip, server_port))
        print("Connected to the server.")

        screen_thread = threading.Thread(target=send_screen, args=(client_socket,))
        command_thread = threading.Thread(target=receive_commands, args=(client_socket,))

        screen_thread.start()
        command_thread.start()

        screen_thread.join()
        command_thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")