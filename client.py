import socket,os



client_soc = socket.socket()
client_soc.connect(("127.0.0.1", 5679))

client_soc.send("did you get it?")


#client_soc.close()





