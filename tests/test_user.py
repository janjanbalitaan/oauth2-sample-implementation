class TestUser:
    users = []
    refresh_tokens = []
    access_tokens = []

    def test_create(
        self,
        client,
    ):
        body = {
            "username": "myuser",
            "password": "mypassword",
        }
        response = client.post(
            '/api/users',
            json=body
        )
        
        assert response.status_code == 201
        data = response.json()
        assert body["username"] == data["username"]
        assert "password" not in data
        assert data["id"]
        self.users.append(
            {
                **data,
                **body,
            }
        )
    
    def test_login(
        self,
        client
    ):
        body = {
            "grant_type": "password",
            "username": self.users[0]["username"],
            "password": self.users[0]["password"],
        }
        response = client.post(
            '/api/oauth2/token',
            json=body
        )

        assert response.status_code == 200
        data = response.json()
        assert data["access_token"]
        assert data["access_token_expiration"]
        assert data["refresh_token"]
        assert data["refresh_token_expiration"]
        self.access_tokens.append(data["access_token"])
        self.refresh_tokens.append(data["refresh_token"])

    def test_update(
        self, 
        client
    ):
        username = "myupdatedusername"
        password = "myupdatedpassword"
        # update username
        body = {
            "username": username
        }
        response = client.put(
            f'/api/users/{self.users[0]["id"]}',
            json=body,
            headers={
                "Authorization": f'Bearer {self.access_tokens[0]}'
            }
        )
        assert response.status_code == 200
        self.users[0]["username"] = body["username"]
        
        # fetch updated data
        response = client.get(
            f'/api/users?id={self.users[0]["id"]}',
            headers={
                "Authorization": f'Bearer {self.access_tokens[0]}'
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == self.users[0]["id"]
        assert data[0]["username"] == body["username"]

        # update password
        body = {
            "password": password
        }
        response = client.put(
            f'/api/users/{self.users[0]["id"]}',
            json=body,
            headers={
                "Authorization": f'Bearer {self.access_tokens[0]}'
            }
        )
        assert response.status_code == 200
        self.users[0]["password"] = body["password"]

        body = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        response = client.post(
            '/api/oauth2/token',
            json=body
        )

        assert response.status_code == 200
        data = response.json()
        assert data["access_token"]
        assert data["access_token_expiration"]
        assert data["refresh_token"]
        assert data["refresh_token_expiration"]
        self.access_tokens.append(data["access_token"])
        self.refresh_tokens.append(data["refresh_token"])

    def test_get(
        self,
        client,
    ):
        # fetch all
        response = client.get(
            f'/api/users',
            headers={
                "Authorization": f'Bearer {self.access_tokens[0]}'
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        
        # fetch by id
        response = client.get(
            f'/api/users?id={self.users[0]["id"]}',
            headers={
                "Authorization": f'Bearer {self.access_tokens[0]}'
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == self.users[0]["id"]
        assert data[0]["username"] == self.users[0]["username"]
        
        # fetch by username
        response = client.get(
            f'/api/users?username={self.users[0]["username"]}',
            headers={
                "Authorization": f'Bearer {self.access_tokens[0]}'
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == self.users[0]["id"]
        assert data[0]["username"] == self.users[0]["username"]

    
    def test_delete(
        self, 
        client
    ):
        for user in self.users:
            response = client.delete(
                f'/api/users/{user["id"]}',
                headers={
                    "Authorization": f'Bearer {self.access_tokens[0]}'
                }
            )
            assert response.status_code == 200