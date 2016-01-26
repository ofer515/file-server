import socket
import os
import thread

allowed_files = ['txt', 'png', 'jpg','doc', 'docx']


def files_available(files_exist):
    file_list = []
    for file_name in files_exist:
        file_type = file_name.split('.')[-1]
        if file_type in allowed_files:
            file_list.append(file_name)
    if file_list == []:
        return "no file available"
    else:
        file_list = str(file_list).replace("[", "")
        file_list = str(file_list).replace("]", "")
        file_list = str(file_list).replace("'", "")
        print file_list
        return str(file_list)


#socket set up and where all connections are formed and receive a thread
def main(port):

    ser_socket = socket.socket()
    ser_socket.bind(("127.0.0.1", port))
    ser_socket.settimeout(100)
    ser_socket.listen(10)

    while True:
        try:
            client_socket, client_address = ser_socket.accept()
            handle_thread = thread.start_new_thread(handle_connection, ((client_socket,ser_socket)),)
            if handle_thread:
                print "saved file"

        except:
            pass


#the server receive the file and checks it
def recv_files(client_soc):
    try:
        ack_msg = client_soc.recv(1024)
        print(ack_msg.split(":"))
        if "sending file name:" in ack_msg:
            f_name = str(ack_msg.split(":", 1)[-1])
            print(f_name)
            if f_name.split(".")[-1] not in allowed_files:
                client_soc.close()
            new_file = open(f_name, 'wb')
            msg = str("receiving file name: "+f_name)
            print msg
            up_file = client_soc.recv(1024)
            print "receiving...."
            while up_file:
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
        if str(e) == "[Errno 10054] An existing connection was forcibly closed by the remote host":
            print("user disconnected")
        else:
            print e


def send_file(client_soc):
    client_soc.send("files available to download: ")
    client_soc.send(files)
    file_name = client_soc.recv(1024)
    if file_name in files:
        file_to_send = open(file_name, 'rb')
        temp_holder = file_to_send.read(1024)
        while temp_holder:
            client_soc.send(temp_holder)
            temp_holder = file_to_send.read(1024)
        print "send successfully"
        client_soc.close()
    else:
        client_soc.send("no such file, don't bug me")
        print "closed connection due to incorrect file name"
        client_soc.close()


#every newly formed connection and then sent to the function it wishes to preform
def handle_connection(client_soc, ser_socket):
    try:
        client_soc.setblocking(100)
        soc_status = True
        print "new connection"
        client_soc.send("Approved")
        print "Approved"
        request = client_soc.recv(1024)
        if request in function:
            function[request](client_soc)
        else:
            print "closed connection"
            client_soc.send("closed connection")
            ser_socket.close()
    except Exception as e:
        if str(e) == "[Errno 10054] An existing connection was forcibly closed by the remote host":
            print("user disconnected")
        else:
            print e


function = {"upload": recv_files,
            "download": send_file}

if __name__ == "__main__":
    port_recv = 56990
    files = files_available(os.listdir(os.curdir))
    main(port_recv)






