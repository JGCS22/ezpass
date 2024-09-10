import json
import sys
import string
import secrets
import os
import base64
from libraries.pandas import pandas as pd
from libraries.tabulate import tabulate
from libraries.getpass_asterisk.getpass_asterisk import getpass_asterisk
from libraries.cryptography.fernet import Fernet
from libraries.cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from libraries.cryptography.hazmat.primitives import hashes
from libraries.cryptography.exceptions import InvalidSignature
from libraries.cryptography.fernet import InvalidToken
from libraries.cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode