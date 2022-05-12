import socket
from datetime import datetime

HOST = '192.168.0.29'
PORT = 80#8888

#소켓 연결
server_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#현재 서버 ip
print("IP Address(Internal) : ",socket.gethostbyname(socket.gethostname()))

server_socket.bind((HOST, PORT))

# 서버가 클라이언트의 접속을 허용하도록 합니다. 
server_socket.listen()

# accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다. 
client_socket, addr = server_socket.accept()

# 접속한 클라이언트의 주소
print('Connected by', addr)

#서버이름
ServerName = '[컴퓨터네트워크 중간과제] 권부연(20203030)'

#request로 입력한 값에 따라 response 메세지를 주고 파일 동작을 하는 함수입니다.
def response(data):

    try:
        #request 메시지를 분석합니다.
        request_data = data.decode().split('\\r\\n')
        
        request_line = request_data[0].split()#request line
        request_method = request_line[0]
        request_version = request_line[2]
        
        request_header={}                   #request header
        request_bodyStart=0#body 구분을 위한 변수
        for header in request_data:
            request_bodyStart+=1
            if header == '':
                break
            if header != request_data[0]:
                k = header.split(':')
                request_header[k[0].strip()] = ':'.join(k[1:]).strip()

        #HTTP 버전을 확인합니다.
        if not request_version in ['HTTP/1.0','HTTP/1.1','HTTP/2']:
            response_data = f"{request_version} 505 HTTP version Not supported\r\n\r\n"

        #파일을 읽어오게 구현한 GET입니다.
        #response 메세지로 ServerName과 host, date를 표시합니다.
        elif request_method == "GET":
        
            try:
                file = open('.'+request_line[1].strip(), 'rt', encoding='utf-8')
                response_data = f"{request_version} 200 OK\r\n ServerName : {ServerName}\r\n Host : {request_header['Host']}\r\n Date : {datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST')}\r\n\r\n"+file.read()+"\r\n\r\n"
                file.close()
            except:
                response_data = f"{request_version} 404 not found\r\n\r\n"

        #ServerName과 date 그리고,request의 header들을 표시합니다.   
        elif request_method == "HEAD":
            response_data = f"{request_version} 200 OK\r\n ServerName : {ServerName}\r\n Date : {datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST')}\r\n"
            for key,item in request_header.items():
                response_data += f"{key} : {item}\r\n"
            response_data += "\r\n"            

        #파일을 생성할 수 있게한 POST입니다.
        #response 메세지로 ServerName과 Location, date를 표시합니다.
        elif request_method == "POST":
            try:
                file = open('.'+request_line[1].strip(), 'wt', encoding='utf-8')
                file.write('\r\n'.join(request_data[request_bodyStart:]))
                response_data = f"{request_version} 200 OK\r\n ServerName : {ServerName}\r\n Location : {'.'+request_line[1].strip()}\r\n Date : {datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST')}\r\n\r\n"
                file.close()
            except:
                response_data = f"{request_version} 400 bad request\r\n\r\n"

        #파일을 갱신할 수 있게한 PUT입니다. python특성상 POST와 동일합니다.
        #response 메세지로 ServerName과 Location, date를 표시합니다.    
        elif request_method == "PUT":
            try:
                file = open('.'+request_line[1].strip(), 'wt', encoding='utf-8')
                file.write('\r\n'.join(request_data[request_bodyStart:]))
                response_data = f"{request_version} 200 OK\r\n ServerName : {ServerName}\r\n Location : {'.'+request_line[1].strip()}\r\n Date : {datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST')}\r\n\r\n"
                file.close()
            except:
                response_data = f"{request_version} 400 bad request\r\n\r\n" 
            
        else:
            response_data = f"{request_version} 400 bad request(not found method)\r\n\r\n"
    
    except:

        return f"400 bad request\r\n"

    return response_data


# 무한루프를 돌면서 
while True:

    # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다. 
    data = client_socket.recv(65535)


     
    # end를 수신하면 루프를 중지합니다. 
    if data.decode() == "end":
        break
     


    # 수신받은 문자열을 출력합니다.
    print('Received from', addr, data.decode())


    # 받은 문자열을 다시 클라이언트로 전송해줍니다.(에코) 
    client_socket.send(response(data).encode())


# 소켓을 닫습니다.
client_socket.close()
server_socket.close()
