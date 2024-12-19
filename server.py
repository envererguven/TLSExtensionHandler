import socket
import ssl
import base64

# Define the custom extension type
CUSTOM_EXTENSION_TYPE = 1000

def extract_msisdn_from_extensions(extensions):
    for ext_type, ext_data in extensions:
        if ext_type == CUSTOM_EXTENSION_TYPE:
            msisdn = base64.b64decode(ext_data).decode('utf-8')
            return msisdn
    return None

def handle_client(client_socket):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='/app/certs/server.crt', keyfile='/app/certs/server.key')
    
    conn = context.wrap_socket(client_socket, server_side=True)
    
    extensions = conn.getpeercert(binary_form=True)['extensions']
    msisdn = extract_msisdn_from_extensions(extensions)
    
    if msisdn:
        print(f"Extracted MSISDN: {msisdn}")
    
    response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
    <html>
    <head><title>MSISDN Info</title></head>
    <body>
    <h1>MSISDN Information</h1>
    <p>Extracted MSISDN: {msisdn}</p>
    </body>
    </html>"""
    
    conn.send(response.encode('utf-8'))
    conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8443))
    server_socket.listen(5)
    
    print("Server listening on port 8443")
    
    while True:
        client_socket, addr = server_socket.accept()
        handle_client(client_socket)
    
if __name__ == '__main__':
    main()