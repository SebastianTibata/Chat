import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Configuración de la ventana
root = tk.Tk()
root.title("Cliente de Chat")
root.geometry("500x450")
root.configure(bg="#2C2F33")

# Elementos de la interfaz
title_label = tk.Label(root, text="Chat Cliente", font=("Arial", 16, "bold"), fg="white", bg="#2C2F33")
title_label.pack(pady=10)

chat_text = scrolledtext.ScrolledText(root, state='disabled', width=55, height=15, bg="#23272A", fg="lime", insertbackground="white")
chat_text.pack(pady=5)

input_frame = tk.Frame(root, bg="#2C2F33")
input_frame.pack(pady=5)

msg_entry = tk.Entry(input_frame, width=40, bg="#40444B", fg="white")
msg_entry.grid(row=0, column=0, padx=5)

send_button = tk.Button(input_frame, text="Enviar", state='disabled', bg="#555555", fg="white", width=10, height=1, font=("Arial", 10, "bold"), bd=0)
send_button.grid(row=0, column=1, padx=5)

button_frame = tk.Frame(root, bg="#2C2F33")
button_frame.pack(pady=10)

active_color = "#43B581"
disabled_color = "#555555"

connect_button = tk.Button(button_frame, text="Conectar", bg=active_color, fg="white", width=15, height=2, font=("Arial", 10, "bold"), bd=0)
connect_button.grid(row=0, column=0, padx=5)

disconnect_button = tk.Button(button_frame, text="Desconectar", state='disabled', bg=disabled_color, fg="white", width=15, height=2, font=("Arial", 10, "bold"), bd=0)
disconnect_button.grid(row=0, column=1, padx=5)

# Variables globales
client_socket = None
connected = False

def log(message):
    "Muestra mensajes en la interfaz"
    chat_text.config(state='normal')
    chat_text.insert(tk.END, message + "\n", "log_color")
    chat_text.config(state='disabled')
    chat_text.yview(tk.END)
    chat_text.tag_config("log_color", foreground="yellow")

def connect_to_server():
    "Conecta al servidor y habilita los botones"
    global client_socket, connected
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 8080))
        connected = True
        log("[CONECTADO]")

        connect_button.config(state='disabled', bg=disabled_color)
        disconnect_button.config(state='normal', bg="#F04747")
        send_button.config(state='normal', bg="#7289DA")

        threading.Thread(target=receive_messages, daemon=True).start()

    except Exception as e:
        log(f"[ERROR] No se pudo conectar: {e}")

def receive_messages():
    "Recibe mensajes del servidor."
    global connected
    while connected:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            if not response:
                break
            log(f"Servidor: {response}")
        except:
            break

def send_message(event=None):
    "Envía un mensaje al servidor."
    global connected
    if connected:
        msg = msg_entry.get()
        if msg:
            client_socket.send(msg.encode('utf-8'))
            log(f"Yo: {msg}")
            msg_entry.delete(0, tk.END)

def disconnect_from_server():
    "Desconecta del servidor."
    global connected
    if connected:
        connected = False
        client_socket.close()
        log("[DESCONECTADO]")
        messagebox.showerror("Error", "Desconectado del servidor")

        connect_button.config(state='normal', bg=active_color)
        disconnect_button.config(state='disabled', bg=disabled_color)
        send_button.config(state='disabled', bg=disabled_color)

# Asignar funciones a los botones
connect_button.config(command=connect_to_server)
disconnect_button.config(command=disconnect_from_server)
send_button.config(command=send_message)
msg_entry.bind("<Return>", send_message)

# Ejecutar la interfaz
root.mainloop()
