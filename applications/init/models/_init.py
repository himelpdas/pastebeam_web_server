from pymongo import MongoClient
_client = MongoClient()
_database = _client.test_database
MONGO_ACCOUNTS = _database.auth_user

import bson.json_util as json
from bson.binary import Binary

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import HMAC,SHA512

class SecureRSAKeyPair(object):
    random_gen = Random.new().read
    def __init__(self, password, pbkdf2 = False, strength = 2048):
        self.password = password
        self.key = RSA.generate(strength, self.random_gen)
        self.public_key = None
        self.private_key = None
        self.passphrase = None
        self.salt = None
        if pbkdf2:
            self.salt = self.random_gen(8) #never reuse salt again to generate a new key derivation
            self.createPassphrase()
        self.generate()
    def createPassphrase(self):
        """
        ensure the key derivation hash function is different from web2py's, or else the key will match the one on server
        dkLen should be 24 since the private key encrypts via 3DES CBC
        """
        self.passphrase = PBKDF2(self.password, self.salt, dkLen=24, count=1000, prf=lambda p, s: HMAC.new(p, s, SHA512).digest()).encode("hex")
    def generate(self):
        self.private_key = self.key.exportKey(passphrase = self.passphrase or self.password)
        self.public_key = self.key.publickey().exportKey()


#MUST BE KEPT OUTSIDE CALLBACK FUNCTION!
import zmq
publisher_context = zmq.Context()
publisher_socket = publisher_context.socket(zmq.PUB)
publisher_socket.connect("tcp://localhost:%s" % 8882)