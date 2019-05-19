crt_storage = 'data/certificates/'

root_cert = crt_storage + 'ca-root.pem'

# certificate if you run the program as user
certificate = crt_storage + 'certificate-alice-pub.pem'
priv_key = crt_storage + 'certificate-alice-key.pem'

# certificate if you run the program as server
server_certificate = crt_storage + 'certificate-localhost-pub.pem'
server_priv_key = crt_storage + 'certificate-localhost-key.pem'
