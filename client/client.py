import socket
import os

allowed_files = ['txt', 'png', 'jpg','doc', 'docx']



#showing receiving all file in dir and returning a list of allowed files(see dictionary)
def files_available(files):
    file_list = []
    for file_name in files:
        file_type = file_name.split('.')[-1]
        if file_type in allowed_files:
            file_list.append(file_name)
    if file_list == []:
        return "no file available"
    return file_list


#in the works, will allow to download file from server
def recv_file(client_soc):
    try:
        client_soc.send("download")
        print "sent request to server"
        data = client_soc.recv(1024)
        list_of_files = client_soc.recv(1024)
        print data, list_of_files

        f_name = raw_input("Enter the file name you wish to download")
        client_soc.send(f_name)
        new_file = open(f_name, 'wb')
        msg = str("receiving file name: "+f_name)
        print msg
        down_file = client_soc.recv(1024)
        while down_file:
            print "receiving...."
            new_file.write(down_file)
            down_file = client_soc.recv(1024)
        new_file.close()
        print "received file and saved"
        client_soc.close()
    except Exception as e:
        print e


#receiving the file(after it has been checked) you wish to download and socket, uploads it to server
def send_file(up_file_name, client_soc):

    up_file = open(up_file_name, 'rb')
    temp_holder = up_file.read(1024)
    while temp_holder:
        client_soc.send(temp_holder)
        temp_holder = up_file.read(1024)
    print "send successfully"
    client_soc.close()


#where the user start the progrem and choose which function he wishes to preform
def main(file_list):

    while True:
        option = int(raw_input("upload(1), download(2) or exit(3) ?: "))
        client_soc = socket.socket()
        client_soc.connect(("127.0.0.1", 56990))
        data = client_soc.recv(1024)

        if data == "Approved":
            print "Approved"
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
            elif option == 2:
                recv_file(client_soc)
            elif option == 3:
                print("closing connection")
                client_soc.close()
                break
        else:
            print "server is down or too busy "
            print data

        client_soc.close()



if __name__ == "__main__":
    main(files_available(os.listdir(os.curdir)))




