import socket, sys, time
import ssl


def make_connection(port=9999):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', int(port)))
        s.listen(5)
        print(f"[*] Listening on port {port}")

    except Exception as e:
        print(e)
        sys.exit(1)

    while True:
        try:
            conn, addr = s.accept()
            parse_request(addr[0], port, conn)
        except Exception as e:
            s.close()


import sys

def parse_request(ip_address, port, conn):
    try:
        request = conn.recv(4096)
        header = request.split(b'\n')[0]
        requested_file = request
        requested_file = requested_file.split(b' ')
        url = header.split(b' ')[1]

        hostIndex = url.find(b"://")
        if hostIndex == -1:
            temp = url
        else:
            temp = url[(hostIndex + 3):]

        portIndex = temp.find(b":")
        serverIndex = temp.find(b"/")

        if serverIndex == -1:
            serverIndex = len(temp)

        webserver = ""
        port = -1
        if portIndex == -1 or serverIndex < portIndex:
            port = 80
            webserver = temp[:serverIndex]
        else:
            port = int((temp[portIndex + 1:])[:serverIndex - portIndex - 1])
            webserver = temp[:portIndex]

        requested_file = requested_file[1]
        print("Requested File ", requested_file)

        target = webserver.replace(b"http://", b"").decode()

        try:
            with open('blacklist/blacklistIP.txt', 'rb') as handle:
                for line in handle.readlines():
                    if line.decode().strip() == target.strip():
                        print("Ip is blacklisted.")
                        conn.close()
                        sys.exit(1)
        except Exception as e:
            print(e)

        try:
            with open('blacklist/blacklistDomain.txt', 'rb') as handle:
                for line in handle.readlines():
                    if line.decode().strip() == target.strip():
                        print("Domain is blacklisted.")
                        conn.close()
                        sys.exit(1)
        except Exception as e:
            print(e)

        method = request.split(b" ")[0]

        if method == b"CONNECT":
            print("https request")
            print(requested_file)
            https_proxy(ip_address, 443, requested_file, request, webserver, conn)
        elif method == b"GET":
            print("http request")
            print(requested_file)
            http_proxy(ip_address, 80, requested_file, request, webserver, conn)
        else:
            print("Unsupported method")
            conn.close()

    except Exception as e:
        pass


def http_proxy(ip_address, port, requested_file, request, webserver, conn):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    requested_file = requested_file.replace(b".", b"_").replace(b"http://", b"_").replace(b"/", b"")
    try:
        with open(b'cache/' + requested_file, 'rb') as handle:
            print(f"Cache Hit for {requested_file}")
            content = handle.read()
            conn.send(content)
        handle.close()

    except Exception as e:
        soc.connect((webserver, int(port)))
        print(f"Cache Miss for {requested_file}")
        soc.send(request)
        time.sleep(2)
        content = soc.recv(4096)
        with open(b'cache/' + requested_file, 'wb') as handle:
            handle.write(content)
        print("Received content:", content) # print first 100 bytes of content

        conn.send(content)
        print(" Request of client " + str(ip_address) + " completed...")
        soc.close()
        handle.close()





def https_proxy(ip_address, port, requested_file, request, webserver, conn):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()

    requested_file = requested_file.replace(b".", b"_").replace(b"https://", b"_").replace(b"/", b"")
    try:
        with open(b'cache/' + requested_file, 'rb') as handle:
            print(f"Cache Hit for {requested_file}")
            content = handle.read()
            conn.send(content)
        handle.close()

    except Exception as e:
        with socket.create_connection((webserver, 443)) as soc:
            with context.wrap_socket(soc, server_hostname=webserver) as ssock:
                ssock.sendall(request)
                print(f"Cache Miss for {requested_file}")
                content = b''
                while True:
                    data = ssock.recv(4096)
                    if not data:
                        break
                    content += data
                print("Received content:", content[:100]) # print first 100 bytes of content
                with open(b'cache/' + requested_file, 'wb') as handle:
                    handle.write(content)

                conn.send(content)
                print("Request of client " + str(ip_address) + " completed...")





if __name__ == "__main__":
    make_connection()



