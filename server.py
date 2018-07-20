#Bibliotecas
from socket import * 
from threading import Thread
import os

#array onde ficarao guardadas as infos dos clientes
clients = []

#string contendo lista de comandos disponiveis
command_list = "\n/all lista todos os usuarios ativos\n/help mostra comandos\n/clear limpa a janela\n/quit sair do chat\n/name Apelido_Novo \n"

#funcao para lidar com o setup inicial do server
def server_setup(host,port):
	server_sock = socket(AF_INET,SOCK_STREAM) #usado para conexao tcp
	server_sock.bind((host,port)) #une host e porta
	server_sock.listen(1) #pronto para receber conexoes
	
	#msg de greetings do server
	print ("server online aguardando conexoes na porta: %d " % (port))
	t_index = 0; #contador das threads

	#enquanto server online
	try:
		while True:
			
			conn_socket, addr = server_sock.accept() #aceitando conexões
			
			#argumentos do array de clientes
			#(socket,nick,status(0=conectado, -1=desconectado),IP)
			clients.append([conn_socket,0,0,addr])
			
			#cria thread para lidar com os users
			t = Thread(target=client_handler, args=(conn_socket,t_index,))
			t.start()  #dispara a thread
			t_index += 1 #incrementa o indice da thread
		
		server_sock.close() #encerra
	except:
		os._exit(0)

#lidando com as msg dos clientes
def client_handler(conn_socket,t_id):
	try:
			#recebe a primeira msg do cliente será o nick
			nickname = conn_socket.recv(1024).decode()
			clients[t_id][1] = nickname # guarda o nick na posição 1 do array de clientes
			conn_socket.send(nickname.encode()) #devolve o nick para confirmar a conexao

			#informa a todos quando um user for conectado
			logged_in = ("O Usuario %s entrou na sala" % clients[t_id][1]) 
			for i in range(0, len(clients)):
				if clients[i][2]==0 and t_id!=i:
					clients[i][0].send(logged_in.encode())
			
			#recebe as msgs do cliente
			while True:	
				message = conn_socket.recv(1024).decode() 
				default_message = "%s disse: %s" % (clients[t_id][1],message)
				
				#printa msg no server apenas para verificar se foram enviandas
				print ("> %s disse: %s"%(clients[t_id][1],message))

				# Change nickname
				if "/name" in message:
					new_name = message.split(' ') #separa no espaço
					#o apelido ficará na posição 1 do array new_name
					change_name_msg = "%s alterou o apelido para: %s" % (clients[t_id][1] , new_name[1])
					clients[t_id][1] = new_name[1] #atualiza o nick do user
					
					#exibe para todos que o nick foi trocado
					for i in range(0, len(clients)):
						if clients[i][2]==0:
							clients[i][0].send(change_name_msg.encode())

				#lista todos os clientes conectados
				elif "/all" in message: 
					for i in range(0, len(clients)):
						if clients[i][2]==0:
							send_list = "[Nome: %s | IP: %s] "%(clients[i][1],clients[i][3]) 
							clients[t_id][0].send(send_list.encode()) #envia para o cliente
				
				#lista os comandos disponiveis
				elif "/help" in message:
					commands = "Lista de comandos << %s" % command_list
					clients[t_id][0].send(commands.encode()) #envia para o user
				
				#se a msg do cliente /quit encerra a conexao e envia para todos a msg que o user foi desconectado
				elif "/quit" in message:
					logged_out = ("%s saiu da sala" % clients[t_id][1]) 
					#envia msg para todos os users que o cliente X desconctou
					for i in range(0, len(clients)):
						if clients[i][2]==0:
							clients[i][0].send(logged_out.encode())
					clients[t_id][2]=-1 #muda o status de conectado para desconectado
					break

				elif "/clear" in message:
					clients[t_id][0].send("/clear".encode()) #envia para o user
				
				#caso mensagem nao seja nenhum dos comandos disponiveis envia msg para todos os users
				else:
					for i in range(0, len(clients)):
						if clients[i][2]==0:
							clients[i][0].send(default_message.encode())
			
			conn_socket.close() #fecha conexao
	except:
		os._exit(0)

if __name__ == '__main__':
	host = '' 
	port = 13000 
	print('-- Server Online --')
	server_setup(host,port)