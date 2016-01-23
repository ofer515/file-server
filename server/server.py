import socket
import os
import thread




ser_socket = socket.socket()


def main(port):
    ser_socket.bind(("127.0.0.1", port))
    ser_socket.settimeout(100)
    ser_socket.listen(10)

    while True:
        try:
            client_socket, client_address = ser_socket.accept()
            handle_thread = thread.start_new_thread(handle_connection, ((client_socket, client_address)),)
            if handle_thread:
                print "saved file"

        except:
            pass


def recv_files(client_soc):
    try:
        ack_msg = client_soc.recv(1024)
        print(ack_msg.split(":"))
        if "sending file name:" in ack_msg:
            f_name = str(ack_msg.split(":", 1)[-1])
            print(f_name)
            new_file = open(f_name, 'wb')
            msg = str("receiving file name: "+f_name)
            print msg
            up_file = client_soc.recv(1024)
            while up_file:
                print "receiving...."
                new_file.write(up_file)
                up_file = client_soc.recv(1024)
            new_file.close()
            print "received file and saved"
            client_soc.close()

        else:
            client_soc.send("not in protocol")
            print "not in protocol, try reconnecting"
            client_soc.close()
    except Exception as e:
        if e == "[Errno 10054] An existing connection was forcibly closed by the remote host":
            print("user disconnected")
        else:
            print e



def handle_connection(client_soc, client_addr):
    try:
        client_soc.setblocking(100)
        soc_status = True
        print "new connection"
        client_soc.send("Approved")
        print "Approved"
        request = client_soc.recv(1024)
        if request == "upload":
            recv_files(client_soc)
        elif request is "download":
            pass
        else:
            ser_socket.close()
    except Exception as e:
        if e == "[Errno 10054] An existing connection was forcibly closed by the remote host":
            print("user disconnected")
        else:
            print e





if __name__ == "__main__":
    port_recv = 5679
    main(port_recv)






