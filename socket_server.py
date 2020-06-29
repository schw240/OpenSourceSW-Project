import socket
import select
import time

server_addr = '192.168.0.2', 9000

# Create a socket with port and host bindings
def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    try:
        s.bind(server_addr)
    except socket.error as msg:
        print(msg)
    return s


# Establish connection with a client
def setupConnection(s):
    s.listen(5)     # Allows five connections at a time
    print("Waiting for client")
    conn, addr = s.accept()
    return conn


# Get input from user
def GET_TXT():
    reply = input("Reply: ")
    return reply


def sendFile(filename, conn):
    f = open(filename, 'rb')
    line = f.read(32)

    print("Beginning File Transfer")
    while line:
        conn.send(line)
        line = f.read(32)
    f.close()
    conn.send(bytes("Transfer Complete", 'utf-8'))
    print("Transfer Complete")


def receiveFile(filename, conn):

    print("Beginning File Receive")
    f = open(filename, 'wb')
    line = conn.recv(8192)
    while True:
        f.write(line)
        line = conn.recv(8192)
        if bytes("DONE", 'utf-8') in line:
            break

    f.close()
    conn.send(bytes("Receive Complete", 'utf-8'))
    print("Receive Complete")



# Loop that sends & receives data
def dataTransfer(conn, s, mode):
    while True:
        # Send a File over the network
        if mode == "SEND":
            filename = "Serverfile.png"
            # filename = conn.recv(32)
            # filename = filename.decode('utf-8')
            # filename.strip()
            print("Requested File: ", filename)
            sendFile(filename, conn)
            # conn.send(bytes("1", 'utf-8'))
            # time.sleep(0.1)
            conn.send(bytes("DONE", 'utf-8'))
            break

        # Chat between client and server
        elif mode == "GET":
            # Receive Data
            filename = "Clientfile.png"
            # filename = conn.recv(8192)
            # filename = filename.decode('utf-8')
            # filename.strip()
            print("Receive File: ", filename)
            receiveFile(filename, conn)
            break
            # Endmark needed?
            conn.send(bytes("Receive Complete", 'utf-8'))


BUF_SIZE = 32
FUNCTION_CONTROL = 0

sock = setupServer()
c_sock = setupConnection(sock)
print("Connecting Established")

while True:
    try:
        if FUNCTION_CONTROL == 1 :
            dataTransfer(c_sock, sock, "CHAT")
            FUNCTION_CONTROL = 0

        elif FUNCTION_CONTROL == 2 :
            # readBuf = c_sock.recv(BUF_SIZE)
            dataTransfer(c_sock, sock, "SEND")
            FUNCTION_CONTROL = 0
            readBuf = c_sock.recv(BUF_SIZE)
            c_sock.send(bytes("Transfer complete", 'utf-8'))

        elif FUNCTION_CONTROL == 3 :
            dataTransfer(c_sock, sock, "GET")
            FUNCTION_CONTROL = 0
            # readBuf = c_sock.recv(BUF_SIZE)
            # c_sock.send(bytes("Receive Complete", 'utf-8'))

        readBuf = c_sock.recv(BUF_SIZE)
        print("Client :", readBuf.decode('utf-8'))

        if str(readBuf, 'utf-8') == 'chat':
            FUNCTION_CONTROL = 1
            print("Chat mode")

        elif str(readBuf, 'utf-8') == 'transfer':
            FUNCTION_CONTROL = 2
            print("file transfer mode")

        elif str(readBuf, 'utf-8') == 'get' :
            FUNCTION_CONTROL = 3
            print("file receive mode")

        elif str(readBuf, 'utf-8') == 'reset':
            FUNCTION_CONTROL = 0
            c_sock.send(bytes("Do reset", 'utf-8'))
            print("Do reset")

        elif str(readBuf, 'utf-8') == 'exit' :
            c_sock.close()

        else :
            c_sock.send(bytes("No request arrived", 'utf-8'))


    except:
        break
