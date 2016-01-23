import socket
import os

allowed_files = ['txt', 'png', 'jpg','doc', 'docx']


def files_available(files):
    file_list = []
    for file_name in files:
        file_type = file_name.split('.')[-1]
        if file_type in allowed_files:
            file_list.append(file_name)
    if file_list == []:
        return "no file available"
    return file_list


def send_file(up_file_name, client_soc):
    up_file = open(up_file_name, 'rb')
    temp_holder = up_file.read(1024)
    while temp_holder:
        client_soc.send(temp_holder)
        temp_holder = up_file.read(1024)
    print "send successfully"
    client_soc.close()

def main(file_list):
    client_soc = socket.socket()
    client_soc.connect(("127.0.0.1", 5679))

    data = client_soc.recv(1024)
    if data == "Approved":
        print "Approved"
        while True:

            option = int(raw_input("upload(1), download(2) or exit(3) ?: "))
            if option == 1:
                client_soc.send("upload")
                print "files available to upload"
                print(file_list)
                up_file_name = str(raw_input("file name to send: "))
                if up_file_name in file_list:
                    raw_data = "sending file name:"
                    print(raw_data+" "+up_file_name)
                    client_soc.send(raw_data+up_file_name)
                    print "sending......"
                    send_file(up_file_name, client_soc)
                else:
                    print("no such file is available, try again")
            elif option == "3":
                print("closing connection")
                client_soc.close()
    else:
        print "server is down or too busy "
        print data

    client_soc.close()


if __name__ == "__main__":
    main(files_available(os.listdir(os.curdir)))




