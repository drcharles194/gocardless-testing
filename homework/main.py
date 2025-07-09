import os
from requests_oauthlib import OAuth2Session
from typing import Dict, Optional

class GoCardlessClient:
    def __init__(self, client_id: str = None, client_secret: str = None, redirect_uri: str = None):
        self.client_id = client_id or os.environ.get('GOCARD_CLIENT_ID')
        self.client_secret = client_secret or os.environ.get('GOCARD_SECRET')
        self.redirect_uri = redirect_uri or "https://test.gocardless.com/redirect"
        self.token_url = "https://connect-sandbox.gocardless.com/oauth/access_token"
        self.auth_base_url = "https://connect-sandbox.gocardless.com/oauth/authorize"
        self.access_token = None
        self.organisation_id = None
        self.oauth_client = None

    def initialize_oauth_client(self, scope: list = None) -> None:
        """Initialize the OAuth client with the given scope."""
        if scope is None:
            scope = ["read_write"]
        self.oauth_client = OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=scope
        )

    def get_authorization_url(self) -> str:
        """Get the authorization URL for the OAuth flow."""
        if not self.oauth_client:
            self.initialize_oauth_client()
        authorization_url, _ = self.oauth_client.authorization_url(self.auth_base_url)
        return authorization_url

    def complete_oauth_flow(self, authorization_response: str) -> Dict:
        """Complete the OAuth flow using the authorization response."""
        if not self.oauth_client:
            self.initialize_oauth_client()
            
        token = self.oauth_client.fetch_token(
            token_url=self.token_url,
            authorization_response=authorization_response,
            client_id=self.client_id,
            client_secret=self.client_secret,
            include_client_id=True
        )
        
        self.access_token = token.get('access_token')
        self.organisation_id = token.get('organisation_id')
        return token

    def is_authenticated(self) -> bool:
        """Check if the client is authenticated."""
        return self.access_token is not None and self.organisation_id is not None

class GoCardlessPartner(GoCardlessClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.partner_details = None
        # Check for PARTNER_TOKEN and PARTNER_ORG_ID in environment
        partner_token = os.environ.get('PARTNER_TOKEN')
        partner_org_id = os.environ.get('PARTNER_ORG_ID')
        if partner_token and partner_org_id:
            self.access_token = partner_token
            self.organisation_id = partner_org_id
            print("Using existing partner token and organisation ID from environment")

    def authenticate_partner(self) -> None:
        """Complete the partner authentication flow."""
        # Skip authentication if we already have a token and org ID
        if self.access_token and self.organisation_id:
            print("Already authenticated with partner token")
            return
            
        auth_url = self.get_authorization_url()
        print(f"Visit this URL to authorize the app: {auth_url}")
        
        authorization_response = input("Please copy the URL you were redirected to: ")
        token = self.complete_oauth_flow(authorization_response)
        print("Authentication successful!")
        print(f"Access Token: {self.access_token}")
        print(f"Organisation ID: {self.organisation_id}")

# Example usage
if __name__ == "__main__":
    partner = GoCardlessPartner()
    partner.authenticate_partner()