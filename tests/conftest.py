from fastapi.testclient import TestClient
import pytest

from app import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def user_resource(client):
    users = []
    token = None
    try:
        data = [
            {
                "username": 'test-1',
                "password": "test-1",
            },
            {
                "username": 'test-2',
                "password": "test-2",
            },
            {
                "username": 'test-3',
                "password": "test-3",
            },
        ]

        for d in data:
            response = client.post(
                '/api/users',
                json=d
            )
            j = response.json()
            users.append(
                {
                    **j,
                    **d,
                }
            )

            r = client.post(
                '/api/oauth2/token',
                json={
                    **d,
                    "grant_type": "password",
                }
            )
            k = r.json()
            token = k["access_token"]
        yield users
    except Exception as e:
        print(f"ERROR: user_resource: {e}")
    finally:
        # delete users
        for u in users:
            response = client.delete(
                f'/api/users/{u["id"]}',
                headers={
                    "Authorization": f'Bearer {token}'
                }
            )