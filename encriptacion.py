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
from datetime import datetime
import datetime
from cryptography.hazmat.primitives.asymmetric import padding

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

    def generador_claves():
        clave_privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        clave_publica = clave_privada.public_key()

        return clave_privada, clave_publica
    
    def generador_certificado_raiz():
        clave_privada_raiz, clave_publica_raiz = Encriptar.generador_claves()

        sujeto = ac_raiz = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Comunidad de Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Madrid"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"AC La Liga"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"AC La Liga Autofirmada"),
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
    
    def generador_certificado_intermedio_usuarios(clave_privada_raiz, certificado_raiz):
        
        clave_privada_intermedio_usuarios, clave_publica_intermedio_usuarios = Encriptar.generador_claves()

        sujeto = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Comunidad de Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Madrid"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"AC Florentino Pérez"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"AC Florentino Pérez Firmada"),
        ])

        certificado_intermedio_usuarios = x509.CertificateBuilder().subject_name(
            sujeto
        ).issuer_name(
            certificado_raiz.subject
        ).public_key(
            clave_publica_intermedio_usuarios
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1825)
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
            x509.SubjectKeyIdentifier.from_public_key(clave_publica_intermedio_usuarios),
            critical=False,
        ).add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(certificado_raiz.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value),
            critical=False,
        ).sign(clave_privada_raiz, hashes.SHA256())

        return clave_privada_intermedio_usuarios, clave_publica_intermedio_usuarios, certificado_intermedio_usuarios
    
    def generador_certificado_intermedio_servidor(clave_privada_raiz, certificado_raiz):
        
        clave_privada_intermedio_servidor, clave_publica_intermedio_servidor = Encriptar.generador_claves()

        sujeto = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Comunidad de Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Madrid"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"AC Javier Tebas"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"AC Javier Tebas Firmada"),
        ])

        certificado_intermedio_servidor = x509.CertificateBuilder().subject_name(
            sujeto
        ).issuer_name(
            certificado_raiz.subject
        ).public_key(
            clave_publica_intermedio_servidor
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1825)
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
            x509.SubjectKeyIdentifier.from_public_key(clave_publica_intermedio_servidor),
            critical=False,
        ).add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(certificado_raiz.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value),
            critical=False,
        ).sign(clave_privada_raiz, hashes.SHA256())

        return clave_privada_intermedio_servidor, clave_publica_intermedio_servidor, certificado_intermedio_servidor
    
    def generador_certificado_servidor(clave_privada_intermedio_servidor, certificado_intermedio_servidor):
            
        clave_privada_servidor, clave_publica_servidor = Encriptar.generador_claves()

        sujeto = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Comunidad de Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Colmenarejo"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"AC Madrid Stars"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"AC Madrid Stars Firmada"),
        ])

        certificado_servidor = x509.CertificateBuilder().subject_name(
            sujeto
        ).issuer_name(
            certificado_intermedio_servidor.subject
        ).public_key(
            clave_publica_servidor
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1095)
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None), 
            critical=True,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(u"localhost"),
            ]),
            critical=False,
        ).add_extension(
            x509.ExtendedKeyUsage([
                x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
            ]),
            critical=False,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(clave_publica_servidor),
            critical=False,
        ).add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(
                certificado_intermedio_servidor.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value
            ),
            critical=False,
        ).sign(clave_privada_intermedio_servidor, hashes.SHA256())

        return clave_privada_servidor, clave_publica_servidor, certificado_servidor
                    
    def generador_certificado_cliente(usuario, clave_privada_intermedio_usuarios, certificado_intermedio_usuarios):

        clave_privada_cliente, clave_publica_cliente = Encriptar.generador_claves()

        sujeto = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Comunidad de Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Colmenarejo"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"AC Madrid Stars"),
            x509.NameAttribute(NameOID.COMMON_NAME, f"{usuario}"),
        ])

        certificado_cliente = x509.CertificateBuilder().subject_name(
            sujeto
        ).issuer_name(
            certificado_intermedio_usuarios.subject
        ).public_key(
            clave_publica_cliente
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1095)
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None), 
            critical=True,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(u"localhost"),
            ]),
            critical=False,
        ).add_extension(
            x509.ExtendedKeyUsage([
                x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH,
            ]),
            critical=False,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(clave_publica_cliente),
            critical=False,
        ).add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(
                certificado_intermedio_usuarios.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value
            ),
            critical=False,
        ).sign(clave_privada_intermedio_usuarios, hashes.SHA256())

        return clave_privada_cliente, clave_publica_cliente, certificado_cliente
    
    def verificar_certificado(certificado, certificado_emisor):
        if certificado_emisor != certificado:
            try:
                certificado_emisor.public_key().verify(
                    certificado.signature,
                    certificado.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    certificado.signature_hash_algorithm,
                )
            except Exception as e:
                print(f"La firma del certificado no es válida: {e}")
                return False
            
            ahora = datetime.datetime.now(datetime.timezone.utc)
            if not (certificado.not_valid_before_utc <= ahora <= certificado.not_valid_after_utc):
                print("El certificado está fuera del periodo de validez")
                return False

            return True
        
    def mandar_clave_sesion(clave_publica_cliente, clave_privada_servidor, clave_sesion):
        clave_sesion_mandada = clave_publica_cliente.encrypt(
            clave_sesion,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            )
        )

        hash = hashes.Hash(hashes.SHA256())
        hash.update(clave_sesion)
        hash_clave_sesion = hash.finalize()

        firma = clave_privada_servidor.sign(
            hash_clave_sesion,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )

        return clave_sesion_mandada, firma
    
    def recibir_clave_sesion(clave_sesion_mandada, firma, clave_publica_servidor, clave_privada_cliente):

        try:
            clave_sesion_recibida = clave_privada_cliente.decrypt(
                clave_sesion_mandada,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                )
            )
        except Exception as e:
            print(f"Error al descifrar la clave de sesión: {e}")
            return False

        hash = hashes.Hash(hashes.SHA256())
        hash.update(clave_sesion_recibida)
        hash_clave_sesion = hash.finalize()

        try:
            clave_publica_servidor.verify(
                firma,
                hash_clave_sesion,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
        except Exception as e:
            print(f"Error al verificar la firma de la clave de sesión: {e}")
            return False

        return clave_sesion_recibida
        
    def cifrar_mensaje(mensaje, clave_sesion, clave_privada_remitente):
        mensaje_bytes = mensaje.encode()

        hash = hashes.Hash(hashes.SHA256())
        hash.update(mensaje_bytes)
        hash_mensaje = hash.finalize()

        firma = clave_privada_remitente.sign(
            hash_mensaje,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )

        mensaje_y_firma = mensaje_bytes + b"||" + firma

        nonce = os.urandom(12)
        chacha = ChaCha20Poly1305(clave_sesion)
        mensaje_cifrado = chacha.encrypt(nonce, mensaje_y_firma, None)

        return mensaje_cifrado, nonce
    
    def descifrar_mensaje(mensaje_cifrado, nonce, clave_sesion, clave_publica_remitente):
        chacha = ChaCha20Poly1305(clave_sesion)
        mensaje_y_firma = chacha.decrypt(nonce, mensaje_cifrado, None)

        mensaje_bytes, firma = mensaje_y_firma.split(b"||", 1)

        hash = hashes.Hash(hashes.SHA256())
        hash.update(mensaje_bytes)
        hash_mensaje = hash.finalize()

        try:
            clave_publica_remitente.verify(
                firma,
                hash_mensaje,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
        except Exception as e:
            print(f"Error al verificar la firma del mensaje: {e}")
            return False

        return mensaje_bytes.decode()