import socket,os



client_soc = socket.socket()
client_soc.connect(("127.0.0.1", 5679))

while True:


    data = client_soc.recv(1024)
    if data == "Approved":
        print "Approved"
        raw_data = "sending file name:" + raw_input("file name to send: ")
        print(raw_data)
        client_soc.send("upload")

       # client_soc.send(raw_data)
    else:
        print "no answer"
        print data

client_soc.close()




