import socket,os



client_soc = socket.socket()
client_soc.connect(("127.0.0.1", 5679))
while True:
    client_soc.send("sending file name:" + raw_input("file name to send: "))
    

client_soc.close()





