import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_sockets = []
        self.lock = threading.Lock()  

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"Servidor escuchando en {self.host}:{self.port}")

            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Conexión aceptada de {client_address}")

                with self.lock:
                    self.client_sockets.append(client_socket)

                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.start()

        except Exception as e:
            print(f"Error general en servidor: {e}")

        finally:
            if self.server_socket:
                self.server_socket.close()
                print("Servidor cerrado.")

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print(f"Cliente {client_address} desconectado.")
                    break

                message = data.decode()
                print(f"Cliente {client_address} dice: {message}")

                self.broadcast(message, client_socket)

        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
            print(f"Conexión con {client_address} terminó inesperadamente: {e}")

        except Exception as e:
            print(f"Error inesperado con {client_address}: {e}")

        finally:
            with self.lock:
                if client_socket in self.client_sockets:
                    self.client_sockets.remove(client_socket)
            client_socket.close()
            print(f"Conexión con {client_address} cerrada.")

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client in self.client_sockets[:]: 
                if client != sender_socket:
                    try:
                        client.sendall(message.encode())
                    except Exception as e:
                        print(f"Error enviando a un cliente: {e}")
                        client.close()
                        self.client_sockets.remove(client)

if __name__ == "__main__":
    server = ChatServer()
    server.start()
