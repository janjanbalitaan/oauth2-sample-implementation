import bcrypt
import hashlib
import base64

class Hash:

    def hash_password(
        self,
        password: bytes,
        salt_rounds: int = 12,
    ) -> bytes:
        sha256_digest = hashlib.sha256(password).digest()
        b64_encoded_password = base64.b64encode(sha256_digest)
        salt = bcrypt.gensalt(salt_rounds)

        hashed_password = bcrypt.hashpw(
            b64_encoded_password,
            salt,
        )

        return hashed_password

    def validate_password(
        self,
        password: bytes,
        hashed_password: bytes,
    ) -> bool:
        sha256_digest = hashlib.sha256(password).digest()
        b64_encoded_password = base64.b64encode(sha256_digest)

        return bcrypt.checkpw(b64_encoded_password, hashed_password)