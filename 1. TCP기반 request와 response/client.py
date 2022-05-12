import socket


# 서버 주소
HOST = '192.168.0.29'  
# 포트 번호 
PORT = 80     


# 소켓 객체를 생성합니다.  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 서버에 접속
client_socket.connect((HOST, PORT))

while True:

    data = input()

    
    # end를 수신하면 루프를 중지합니다. 
    if data == 'end':
        break
    

    # 메시지를 전송합니다. 
    client_socket.sendall(data.encode())

    # 메시지를 수신합니다. 
    data = client_socket.recv(65535)
    print('Received >>\r\n', data.decode())


# 소켓을 닫습니다.
client_socket.close()
