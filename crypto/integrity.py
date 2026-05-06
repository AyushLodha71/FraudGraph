import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

'''print(hashlib.algorithms_available)
data = b"e4 e5 Nf4"
h = hashlib.sha256()
h.update(data)
print(h.hexdigest())
'''

def hash_game(moves: str) -> str:
    encoder = hashlib.sha256()
    message = bytes(moves,'utf-8')
    encoder.update(message)
    return encoder.hexdigest()

def verify_game(moves: str, known_hash: str) -> bool:
    encoded_moves = hash_game(moves)
    return encoded_moves == known_hash

print(hash_game(""))
print(hash_game("e4 e5 Nf4"))
print(verify_game("e4 e5 Nf4", hash_game("e4 e5 Nf4")))


def sign_game(game_hash: bytes, private_key) -> bytes:
    signature = private_key.sign(game_hash,ec.ECDSA(hashes.SHA256()))
    return signature

def verify_game_signature(game_hash: bytes, signature: bytes, public_key) -> bool:
    try:
        public_key.verify(signature,game_hash,ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False


private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

game = "e4 e5 Nf3"
game_bytes = bytes(game, 'utf-8')

signature = sign_game(game_bytes, private_key)
print(verify_game_signature(game_bytes, signature, public_key))
print(verify_game_signature(b"", signature, public_key))
