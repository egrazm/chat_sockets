import socket
import threading

class ChatCliente:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print("Error al conectar con el servidor:", e)
            return

        print(f"Conectado a servidor {self.host}:{self.port}")

        escuchar = threading.Thread(target=self.listen_server)
        escuchar.daemon = True
        escuchar.start()

        try:
            self.chat_loop()
        except KeyboardInterrupt:
            print("Interrumpido por el usuario.")
        finally:
            self.client_socket.close()

    def chat_loop(self):
        while True:
            msg = input("yo> ")
            if msg.lower() == "exit":
                break
            self.client_socket.sendall(msg.encode())

    def listen_server(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print("\notro:", data.decode(), "\nyo> ", end="")
            except:
                break

if __name__ == "__main__":
    cliente = ChatCliente()
    cliente.start()
