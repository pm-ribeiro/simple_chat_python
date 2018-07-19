# import libraries
from socket import *
from threading import Thread
import os

#funcao que define o setup inicial do client
def client_setup(host,port):
	cli_sock = socket(AF_INET,SOCK_STREAM)  #cria socket do client
	cli_sock.connect((host, port))  #junta endereços

	#primeira msg será o nick do usuario
	nickname = input('Digite seu apelido: ')
	cli_sock.send(nickname.encode()) #envia o nickname pro server	
	returned_nickname = cli_sock.recv(1024).decode() 
	#server devolve o nickname apenas conferir que o user foi concetado
	
	#greetings msg
	greetings = "~~ Bem vindo %s ~~\n< Para ver a lista de comandos digite /help >" % returned_nickname
	print (greetings)

	#chama funcao que lida com as msg recebidas
	t = Thread(target=received_messages, args=(cli_sock,))
	t.start()

	#lidando com as msg enviadas pelo user
	try:
		while True:
			message = input('') #recebe menssagem do user
			cli_sock.send(message.encode()) #envia msg pro server
			#se a msg do user for close, printa que ele foi desconectado
			if message == "/clear":
				os.system('clear')
			#se a msg do user for close, printa que ele foi desconectado
			if message == "/quit":
				print("Voce saiu da sala.")
				cli_sock.close()  #encerra o socket do cliente
				break
	except:
		os._exit(0)

#função para lidar cm as msg recebidas
#apenas recebe a msg dos users e printa na tela
def received_messages(cli_sock):
	try:
		while True:
			recv_message = cli_sock.recv(1024).decode() 
			print ('>> %s ' % (recv_message)) 
	except:
		os._exit(0);

#-------------------------------------------------------
if __name__ == '__main__':
	host = '192.168.25.5' 
	port = 13000 
	client_setup(host,port)