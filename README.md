# Python Remote Desktop Application

## Overview
This project is a **Remote Desktop Application** written in Python. The application enables screen sharing and complete control of a client machine from a server device. It is a lightweight solution for remote assistance, troubleshooting, or collaborative tasks.

The **client's screen** is streamed to the server in real-time, and the server has full control of the client's mouse and keyboard inputs.

## Features
- **Real-Time Screen Sharing**: The client's screen is streamed to the server with minimal latency.
- **Full Remote Control**:
  - Mouse movements and clicks.
  - Keyboard typing, backspace, and Enter commands.
  - Additional options for double-click and right-click.
- **Dynamic Resolution**: The server adjusts the screen size to match the client's resolution.
- **Intuitive GUI**: A simple, user-friendly interface built with **Tkinter**.

## Requirements
- Python 3.x installed on both the client and server machines.
- Install all required dependencies using the `requirements.txt` file.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abdulrehmangulfaraz/Remote-Desktop.git
   cd Remote-Desktop
   ```

2. **Install dependencies**:
   Run the following command in the terminal to install all required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   - Start the **server** on the controlling device:
     ```bash
     python server.py
     ```
     - Note the IP and Port displayed on the server screen.
   - Start the **client** on the controlled device:
     ```bash
     python client.py
     ```
     - Enter the server's IP and Port when prompted.

## How It Works
1. **Server-Side**:
   - Captures the client's screen data and displays it in a Tkinter window.
   - Allows full control of the client's device via mouse and keyboard inputs.

2. **Client-Side**:
   - Streams the client's screen to the server.
   - Executes control commands received from the server (mouse movements, clicks, and keyboard typing).

### Example Use Case
- The **server device** is your computer, running `server.py`.
- The **client device** is another computer, running `client.py`.
- Once connected, you can see the client's screen on your server device and control it remotely.


## About Me
Hi, I'm Abdulrehman Gulfaraz, a **Computer Science student at UET Lahore**.
Feel free to check out my [LinkedIn profile](https://www.linkedin.com/in/abdulrehman-gulfaraz) for more about my projects and skills!

## Contribution
Contributions are welcome!
- Fork the repository.
- Create a new branch for your feature or fix.
- Submit a pull request explaining your changes.


