from boto3.session import Session
from .helpers import as_bytes
from .helpers import b64_str
from .helpers import from_b64_str
from .aws import kms_client
from .helpers import prefix_alias


def encrypt_bytes(
        plain_text: bytes,
        alias: str,
        region: str = None,
        profile: str = None,
        session: Session = None) -> bytes:
    client = kms_client(region, profile, session)
    alias = prefix_alias(alias)
    data = client.encrypt(KeyId=alias, Plaintext=plain_text)
    return data['CiphertextBlob']


def decrypt_bytes(
        cipher_text: bytes,
        region: str = None,
        profile: str = None,
        session: Session = None) -> bytes:
    client = kms_client(region, profile, session)
    data = client.decrypt(CiphertextBlob=cipher_text)
    return data['Plaintext']


def encrypt(
        plain_text,
        alias,
        region: str = None,
        profile: str = None,
        session: Session = None) -> str:
    plain_text = as_bytes(plain_text)
    data = encrypt_bytes(plain_text, alias, region, profile, session)
    return b64_str(data)


def decrypt(
        cipher_text: str,
        region: str = None,
        profile: str = None,
        session: Session = None):
    cipher_text = from_b64_str(cipher_text)
    data = decrypt_bytes(cipher_text, region, profile, session)
    return data.decode('utf-8')
