from datetime import datetime, timedelta

from utilities.hash import Hash
from utilities.jwt import JWT

class TestUtilities:

    def test_hash(
        self,
    ):
        hash = Hash()
        password = b"testpass"
        password_2 = b"testpass2"
        hashed_password = hash.hash_password(
            password=password,
            salt_rounds=12,
        )
        hashed_password_2 = hash.hash_password(
            password=password_2,
            salt_rounds=12,
        )
        assert hashed_password is not None
        assert type(hashed_password) == bytes
        assert hashed_password != password
        assert hashed_password != hashed_password_2

        is_valid_password = hash.validate_password(
            password=password,
            hashed_password=hashed_password
        )
        assert type(is_valid_password) == bool
        assert is_valid_password

    def test_jwt(
        self,
    ):
        jwt = JWT()
        payload = {
            "test": "test"
        }
        secret = "this is a secret"

        jwt_encoded, exp = jwt.encode(
            payload=payload,
            secret=secret,
            algorithm="HS256",
        )

        assert jwt_encoded is not None
        assert type(jwt_encoded) == str
        assert jwt_encoded
        assert (datetime.now() + timedelta(minutes=29)).timestamp() < exp

        jwt_decoded = jwt.decode(
            token=jwt_encoded,
            secret=secret,
            algorithm="HS256"
        )

        assert jwt_decoded is not None
        assert type(jwt_decoded) == dict
        assert jwt_decoded == payload