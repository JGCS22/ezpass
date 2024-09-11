from base64 import urlsafe_b64encode
from libraries.cryptography.exceptions import InvalidSignature
from libraries.cryptography.fernet import Fernet
from libraries.cryptography.fernet import InvalidToken
from libraries.cryptography.hazmat.primitives import hashes
from libraries.cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from libraries.cryptography.hazmat.backends import default_backend
from libraries.getpass_asterisk.getpass_asterisk import getpass_asterisk
from libraries.pandas import pandas as pd
from libraries.tabulate import tabulate
import base64
import json
import secrets
import string

