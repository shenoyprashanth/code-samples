## X509 Certificates and TLS

### Connect to a remote server and view the certificates.
```
openssl s_client -showcerts -connect www.github.com:443
```
```
    openssl s_client -showcerts -connect www.github.com:443
    Certificate chain
     C = US, ST = California, L = San Francisco, O = "GitHub, Inc.", CN = github.com
     C = US, O = DigiCert Inc, CN = DigiCert TLS Hybrid ECC SHA384 2020 CA1
    -----BEGIN CERTIFICATE-----
    MIIFajCCBP... (Omitted for brevity)
    -----END CERTIFICATE-----
     C = US, O = DigiCert Inc, CN = DigiCert TLS Hybrid ECC SHA384 2020 CA1
     C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
    -----BEGIN CERTIFICATE-----
    MIIEFzCCAv...(Omitted for brevity)
    -----END CERTIFICATE----- 
    SSL handshake has read 2805 bytes and written 380 bytes    
    ---
    New, TLSv1.3, Cipher is TLS_AES_128_GCM_SHA256
    Server public key is 256 bit
    Secure Renegotiation IS NOT supported
    Compression: NONE
    Expansion: NONE
```
- This indicates that a X509 certificate was issued to **GitHub.com** by a certificate authority called **DigiCert.**
- The client and the server as part of handshake have agreed to use TLSv1.3

### Save the certificate locally

```
openssl s_client -showcerts -connect www.github.com:443 | openssl x509 > githubcert.pem
```

### View detailed information about the certificate
```
openssl x509 -in githubcert.pem -text -noout
```

```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            05:18:9a:54:eb:e8:c7:e9:03:e0:ab:0d:92:55:45:de
        Signature Algorithm: ecdsa-with-SHA384
        Issuer: C = US, O = DigiCert Inc, CN = DigiCert TLS Hybrid ECC SHA384 2020 CA1
        Validity
            Not Before: Mar 15 00:00:00 2022 GMT
            Not After : Mar 15 23:59:59 2023 GMT
        Subject: C = US, ST = California, L = San Francisco, O = "GitHub, Inc.", CN = github.com
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key: (256 bit)
                pub:
                    04:4a:b0:93:71:85:21:ec:62:3f:cb:74:c0:46:c8:
                    e7:00:dc:27:4a:32:4b:8a:d5:51:83:08:11:23:52:
                    65:c5:9d:64:75:94:10:9f:99:6d:3f:7b:fb:29:3b:
                    58:b8:37:54:78:4b:b7:3d:1c:77:7e:90:dd:bb:67:
                    23:32:5c:80:d1
                ASN1 OID: prime256v1
                NIST CURVE: P-256
        X509v3 extensions:
            X509v3 Authority Key Identifier:
                keyid:0A:BC:08:29:17:8C:A5:39:6D:7A:0E:CE:33:C7:2E:B3:ED:FB:C3:7A
            X509v3 Subject Key Identifier:
                78:AA:72:C6:71:69:68:14:B5:59:B1:9E:8B:6E:2B:40:87:42:3B:1E
            X509v3 Subject Alternative Name:
                DNS:github.com, DNS:www.github.com
            X509v3 Key Usage: critical
                Digital Signature
            X509v3 Extended Key Usage:
                TLS Web Server Authentication, TLS Web Client Authentication
            X509v3 CRL Distribution Points:
                Full Name:
                  URI:http://crl3.digicert.com/DigiCertTLSHybridECCSHA3842020CA1-1.crl
                Full Name:
                  URI:http://crl4.digicert.com/DigiCertTLSHybridECCSHA3842020CA1-1.crl
            X509v3 Certificate Policies:
                Policy: 2.23.140.1.2.2
                  CPS: http://www.digicert.com/CPS
            Authority Information Access:
                OCSP - URI:http://ocsp.digicert.com
                CA Issuers - URI:http://cacerts.digicert.com/DigiCertTLSHybridECCSHA3842020CA1-1.crt
            X509v3 Basic Constraints:
                CA:FALSE
    Signature Algorithm: ecdsa-with-SHA384
```

**Signature Algorithm: ecdsa-with-SHA384.**
- Take a piece of data. 
- Hash it with SHA384 algorithm. 
- Encrypt the hash with the private key of the server. 
- Anything that is encrypted with the private key can be decrypted with the public key.
- Recompute the hash on the client side. Compare the hashes to ensure that the data is not tampered with.