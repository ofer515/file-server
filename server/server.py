import socket,os
import thread




ser_socket = socket.socket()


def main(port):
    ser_socket.bind(("127.0.0.1", port))
    ser_socket.settimeout(100)
    ser_socket.listen(100)

    while True:
        try:
            client_socket, client_address = ser_socket.accept()
            client_socket.setblocking(20)
            soc_status = True
            print "new connection"
            client_socket.send("Approved")
            print "Approved"
            request = client_socket.recv(1024)
            print "got"
            if request == "upload":
                recv_thread = thread.start_new_thread(recv_files, ((client_socket,)))
            elif request is "download":
                pass
            else:
                ser_socket.close()
        except Exception as e:
            print e


def recv_files(client_soc):
    try:
        ack_msg = client_soc.recv(1024)

        if "sending file name:" in ack_msg:
            f_name = str(ack_msg.split(":", 1)[1])
            msg = str("receiving file name: "+f_name)
            print msg
            print f_name

        else:
            client_soc.send("not in protocol")
            print "not in protocol, try reconnecting"
            client_soc.close()
    except Exception as e:
        print e

    print "waiting for file...."
    file = client_soc.recv(1024)
    nFile = open(fname, 'w+')
    while(file):
        print "receiving...."
        nFile.write(file)
    nFile.close()






if __name__ == "__main__":
    port_recv = 5679
    main(port_recv)






