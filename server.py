import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Configuración de la ventana
root = tk.Tk()
root.title("Servidor de Chat")
root.geometry("500x400")
root.configure(bg="#2C2F33")

# Elementos de la interfaz
title_label = tk.Label(root, text="Servidor de Chat", font=("Arial", 16, "bold"), fg="white", bg="#2C2F33")
title_label.pack(pady=10)

log_text = scrolledtext.ScrolledText(root, state='disabled', width=55, height=15, bg="#23272A", fg="lime", insertbackground="white")
log_text.pack(pady=5)

button_frame = tk.Frame(root, bg="#2C2F33")
button_frame.pack(pady=10)

active_color = "#43B581"
disabled_color = "#555555"

start_button = tk.Button(button_frame, text="Iniciar Servidor", width=15, height=2, font=("Arial", 10, "bold"), bd=0, bg=active_color, fg="white")
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(button_frame, text="Detener Servidor", width=15, height=2, font=("Arial", 10, "bold"), bd=0, bg=disabled_color, fg="white", state='disabled')
stop_button.grid(row=0, column=1, padx=5)

# Variables globales
ip= '127.0.0.1'
puerto = 8080
server_socket = None
running = False
user_count = 0
clients = {}

def log(message):
    "Muestra mensajes en la interfaz gráfica."
    log_text.config(state='normal')
    log_text.insert(tk.END, message + "\n", "log_color")
    log_text.config(state='disabled')
    log_text.yview(tk.END)
    log_text.tag_config("log_color", foreground="yellow")

def handle_client(client_socket, client_address, username):
    "Maneja la comunicación con un cliente."
    log(f"[NUEVA CONEXIÓN] {username} ({client_address[0]}:{client_address[1]}) conectado.")
    
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                log(f"[{username}] {msg}")
                client_socket.send("Mensaje recibido".encode('utf-8'))
            else:
                break
        except:
            break

    client_socket.close()
    del clients[client_socket]
    log(f"[DESCONEXIÓN] {username} ({client_address[0]}:{client_address[1]}) desconectado.")

def server_loop():
    "Loop principal del servidor, acepta clientes en hilos separados."
    global server_socket, running, user_count
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip, puerto))
        server_socket.listen(5)
        log("[SERVIDOR INICIADO] Esperando conexiones")

        while running:
            try:
                client_socket, client_address = server_socket.accept()
                user_count += 1
                username = f"Usuario{user_count}"
                clients[client_socket] = username
                
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, username))
                client_thread.start()
            except OSError:
                break  # Cuando el servidor se detiene, sale del loop

    except Exception as e:
        log(f"[ERROR] No se pudo iniciar el servidor: {e}")
        running = False
        start_button.config(state='normal', bg=active_color)
        stop_button.config(state='disabled', bg=disabled_color)

    server_socket.close()
    log("[SERVIDOR DETENIDO]")

def start_server():
    "Inicia el servidor en un hilo separado."
    global running
    if not running:
        running = True
        threading.Thread(target=server_loop, daemon=True).start()
        start_button.config(state='disabled', bg=disabled_color)
        stop_button.config(state='normal', bg="#F04747")

def stop_server():
    "Detiene el servidor cerrando el socket."
    global running
    if running:
        running = False
        server_socket.close()
        start_button.config(state='normal', bg=active_color)
        stop_button.config(state='disabled', bg=disabled_color)
        log("[SERVIDOR DETENIDO]")

# Asignar funciones a los botones
start_button.config(command=start_server)
stop_button.config(command=stop_server)

# Ejecutar la interfaz
root.mainloop()
