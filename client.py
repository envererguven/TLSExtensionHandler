import socket
import ssl
import base64

# Define the custom extension type
CUSTOM_EXTENSION_TYPE = 1000

def create_custom_extension(msisdn):
    encoded_msisdn = base64.b64encode(msisdn.encode('utf-8'))
    return (CUSTOM_EXTENSION_TYPE, encoded_msisdn)

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('/app/certs/server.crt')
    
    extensions = [create_custom_extension("1234567890")]
    
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname='localhost')
    conn.connect(('localhost', 8443))
    
    conn.do_handshake(extensions=extensions)
    conn.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
    
    response = conn.recv(4096)
    print(response.decode('utf-8'))
    
    conn.close()

if __name__ == '__main__':
    main()