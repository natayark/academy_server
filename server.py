import socket

def load_user_list(file_path):
    user_list = {}
    with open(file_path, 'r') as file:
        file.seek(0)
        for line in file:
            print(line)
            username, password = line.strip().split(':')
            user_list[username] = password
    return user_list

def validate_credentials(username, password, user_list):
    if username in user_list and user_list[username] == password:
        return b"success"
    else:
        return b"failure"

def main():
    # 加载用户列表
    user_list = load_user_list('userlist.txt')
    
    # 创建一个socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定服务器地址和端口
    server_address = ('0.0.0.0', 14059)
    server_socket.bind(server_address)
    
    # 监听连接
    server_socket.listen(1)
    print('waiting')
    
    while True:
        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print('connect from', client_address)
        
        try:
            # 接收客户端发送的数据
            data = client_socket.recv(1024)
            if data:
                # 解析接收到的数据，假设格式为"username:password"
                try:
                    username, password = data.decode('utf-8').split(':')
                    print(f'user: {username}, password: {password}')
                except ValueError:
                    print("Invalid data format received.")
                    client_socket.sendall("failure".encode('utf-8'))
                    continue
                
                # 验证用户名和密码
                response = validate_credentials(username, password, user_list)
                
                # 发送验证结果给客户端
                client_socket.sendall(response)
            else:
                print('no data received')
        finally:
            # 关闭客户端连接
            client_socket.close()

if __name__ == '__main__':
    main()
