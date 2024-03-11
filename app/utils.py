#!/usr/bin/python3
import hmac
import hashlib
import base64
import time
from loguru import logger

def sign_url(url: str, key: str, secret:str) -> str:
    """
    Generate a signed URL by creating a signature using the provided key and secret.

    Args:
        url (str): The URL to report.
        key (str): The access key used for signing.
        secret (str): The secret key used for generating the signature.

    Returns:
        str: The signed URL with the generated signature.
    """
    logger.info('Beginning Signed URL Generation')
    request_type = 'GET'
    content_type = ''
    content_digest = hashlib.md5().digest()
    content_digest = base64.encodebytes(content_digest).decode('utf-8').strip()
        
    request_string = ','.join([request_type, content_type, content_digest, url, str(time.time())])

    secret_bytes = bytearray(secret, encoding='utf-8')
    request_bytes = bytearray(request_string, encoding='utf-8')

    signature = hmac.new(secret_bytes, msg=request_bytes, digestmod=hashlib.sha256).hexdigest()

    signed_url = '%s&signature=%s' % (url, signature)
    logger.success(f'Successfully Signed Url: {signed_url}')
    return signed_url

