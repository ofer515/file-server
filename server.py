import socket,os
import thread




ser_socket = socket.socket()




def main(port):
    ser_socket.bind(("127.0.0.1", port))
    ser_socket.settimeout(20)
    ser_socket.listen(10)

    while True:

        client_socket, client_address = ser_socket.accept()
        try:
            ack_msg = ser_socket.recv(1024)
            if ack_msg.contain("sending file name:"):
                fName = ack_msg.split(":", 1)
                recv_thread = thread.start_new_thread(recv_files, fName)
            else:
                ser_socket.send("not in protocol")
        except socket.timeout:
            ser_socket.send("connection timed out")
            print "connection timed out"
            client_socket.close()

   #send_thread = thread.start_new_thread()

def send_file():
    pass

def recv_files(fname):

    print "waiting for file...."
    file = ser_socket.recv(1024)
    nFile = open(fname, 'w+')
    while(file):
        print "receiving...."
        nFile.write(file)
    nFile.close()






if __name__ == "__main__":
    port_recv = 5679
    main(port_recv)






