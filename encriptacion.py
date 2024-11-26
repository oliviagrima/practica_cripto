import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from datetime import datetime, timedelta, timezone
import datetime

class Encriptar:

    def generador_clave():
        key = Fernet.generate_key()
        return key
    
    def generador_salt(usuario):
        salt = os.urandom(32)
        return salt

    def generador_token(usuario, contraseña, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        token = base64.urlsafe_b64encode(kdf.derive(contraseña))
        return token
    
    def encriptar(fichero, f):
        fichero_cifrado = f.encrypt(fichero)
        return fichero_cifrado
    
    def desencriptar(fichero_cifrado, f):
        fichero = f.decrypt(fichero_cifrado)
        return fichero
    
    def generador_clave_chacha20_poly():
        clave = os.urandom(32)
        return clave

    def encriptar_mensaje(clave, mensaje, num_unico):
        chacha = ChaCha20Poly1305(clave)
        mensaje_cifrado = chacha.encrypt(num_unico, mensaje.encode(), None)
        return mensaje_cifrado

    def desencriptar_mensaje(clave, mensaje_cifrado, num_unico):
        chacha = ChaCha20Poly1305(clave)
        mensaje_descifrado = chacha.decrypt(num_unico, mensaje_cifrado, None)
        return mensaje_descifrado.decode()

    def generador_claves():
        clave_privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        clave_publica = clave_privada.public_key()

        return clave_privada, clave_publica
    
    def generador_certificado_raiz():
        clave_privada_raiz = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        clave_publica_raiz = clave_privada_raiz.public_key()

        sujeto = ac_raiz = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Comunidad de Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Madrid"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"AC Florentino Pérez"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"AC Florentino Pérez Autofirmada"),
        ])

        certificado_raiz = x509.CertificateBuilder().subject_name(
            sujeto
        ).issuer_name(
            ac_raiz
        ).public_key(
            clave_publica_raiz
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), 
            critical=True,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(clave_publica_raiz),
            critical=False,
        ).sign(clave_privada_raiz, hashes.SHA256())
        
        return clave_privada_raiz, clave_publica_raiz, certificado_raiz
    
    def generador_certificado_intermedio1(clave_privada_raiz, certificado_raiz):
        
        clave_privada_ancelotti = rsa.generate_private_key(
            public_exponent=65537, 
            key_size=2048,
        )
        clave_publica_ancelotti = clave_privada_ancelotti.public_key()

        sujeto = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Comunidad de Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Madrid"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"AC Carlo Ancelotti"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"AC Carlo Ancelotti Firmada"),
        ])

        certificado_ancelotti = x509.CertificateBuilder().subject_name(
            sujeto
        ).issuer_name(
            certificado_raiz.subject
        ).public_key(
            clave_publica_ancelotti
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=0), critical=True,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(clave_publica_ancelotti),
            critical=False,
        ).add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(certificado_raiz.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value),
            critical=False,
        ).sign(clave_privada_raiz, hashes.SHA256())

        return clave_privada_ancelotti, clave_publica_ancelotti, certificado_ancelotti
    
    def generador_certificado_intermedio2(clave_privada_raiz, certificado_raiz):
        
        clave_privada_butragueño = rsa.generate_private_key(
            public_exponent=65537, 
            key_size=2048,
        )
        clave_publica_butragueño = clave_privada_butragueño.public_key()

        sujeto = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Comunidad de Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Madrid"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"AC Emilio Butragueño"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"AC Emilio Butragueño Firmada"),
        ])

        certificado_butragueño = x509.CertificateBuilder().subject_name(
            sujeto
        ).issuer_name(
            certificado_raiz.subject
        ).public_key(
            clave_publica_butragueño
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=0), critical=True,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(clave_publica_butragueño),
            critical=False,
        ).add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(certificado_raiz.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value),
            critical=False,
        ).sign(clave_privada_raiz, hashes.SHA256())

        return clave_privada_butragueño, clave_publica_butragueño, certificado_butragueño
    
    