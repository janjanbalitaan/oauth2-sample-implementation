class TestOAuth:
    refresh_tokens = []
    access_tokens = []
    def test_password_grant(
        self,
        client,
        user_resource,
    ):
        body = {
            "grant_type": "password",
            "username": user_resource[0]["username"],
            "password": user_resource[0]["password"],
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

    def test_refresh_token_grant(
        self,
        client,
        user_resource,
    ):
        body = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_tokens[0],
        }
        response = client.post(
            '/api/oauth2/token',
            json=body
        )

        assert response.status_code == 200
        data = response.json()
        assert data["access_token"]
        assert data["access_token_expiration"]
        self.access_tokens.append(data["access_token"])
    
    def test_revoke_all(self, client):
        response = client.delete(
            f'/api/oauth2/revoke?refresh_token=all',
            headers={
                "Authorization": f'Bearer {self.access_tokens[0]}'
            }
        )
        assert response.status_code == 200

    def test_revoke_per_refresh_token(self, client):
        response = client.delete(
            f'/api/oauth2/revoke/{self.refresh_tokens[0]}'
        )
        # added 404 since we call revoke_all before calling this test
        assert response.status_code in [200, 404]