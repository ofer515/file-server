import socket,os
import thread




ser_socket = socket.socket()


def main(port):
    ser_socket.bind(("127.0.0.1", port))
    ser_socket.settimeout(10)
    ser_socket.listen(10)

    while True:
        try:
            client_socket, client_address = ser_socket.accept()
            soc_status = True
            print "new connection"
            client_socket.send("Approved")
            print "Approved"
            request = ser_socket.recv(1024)
            print "got"
            if request == "upload":
                print "?????"
                recv_thread = thread.start_new_thread(recv_files)
            elif request is "download":
                pass
            else:
                ser_socket.close()
        except:
            pass


def recv_files():
    try:
            ack_msg = ser_socket.recv(1024)
            print ack_msg
            if "sending file name:" in ack_msg:
                fName = ack_msg.split(":", 1)[1]
                print fName

            else:
                ser_socket.send("not in protocol")
                print "not in protocol, try reconnecting"
                client_socket.close()
    except Exception as e:
        print e

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






