import gocardless_pro
from typing import Dict
from .main import GoCardlessClient

class GoCardlessOperations:
    def __init__(self, client: GoCardlessClient):
        if not client.is_authenticated():
            raise ValueError("Client must be authenticated before performing operations")
        self.client = client
        self.base_url = "https://api-sandbox.gocardless.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {client.access_token}",
            "GoCardless-Version": "2015-07-06",
            "Content-Type": "application/json"
        }
        self.partner = client
        self.gocardless_pro_client = gocardless_pro.Client(
            access_token=client.access_token,
            environment='sandbox'  # Change to 'live' for production
        )
        self.mandate_id = None
        self.billing_request_id = None

    def create_billing_request_and_flow(self, amount: int, currency: str = "GBP", description: str = None) -> Dict:
        """
        Create a billing request for collecting both mandate and payment.
        
        Args:
            amount: Amount in smallest currency unit (e.g., pence for GBP)
            currency: Three-letter ISO currency code
            description: Optional description for the payment
        
        Returns:
            Dict containing the billing request flow details including the authorization URL
        """
        request_params = {
            "payment_request": {
                "amount": amount,
                "currency": currency,
                "description": description
            },
            "mandate_request": {
                "currency": "GBP"
            }
        }
        billing_request = self.gocardless_pro_client.billing_requests.create(params=request_params)
        self.billing_request_id = getattr(billing_request, 'id')
        
        flow_params = {
            "redirect_uri": "https://example.com/redirect",
            "exit_uri": "https://example.com/exit",
            "links": {
                "billing_request": self.billing_request_id
            }
        }
        flow = self.gocardless_pro_client.billing_request_flows.create(params=flow_params)
        return flow

    def get_billing_request(self, billing_request_id: str = None) -> Dict:
        """
        Get billing request details.
        
        Args:
            billing_request_id: The ID of the billing request to retrieve. If None, uses the stored ID.
            
        Returns:
            Dict containing the billing request details
        """
        if billing_request_id is None:
            billing_request_id = self.billing_request_id
            
        if not billing_request_id:
            raise ValueError("No billing request ID available")
            
        try:
            billing_request = self.gocardless_pro_client.billing_requests.get(billing_request_id)
            
            # Try to get the mandate ID from links
            if hasattr(billing_request, 'links'):
                links = billing_request.links
                # Access the mandate_request_mandate directly from the links object
                if hasattr(links, 'mandate_request_mandate'):
                    self.mandate_id = links.mandate_request_mandate
            
            return billing_request
        except Exception as e:
            print(f"Error retrieving billing request: {str(e)}")
            return None

    def get_mandate(self, mandate_id: str) -> Dict:
        """
        Get mandate details by ID.
        
        Args:
            mandate_id: The ID of the mandate to retrieve
            
        Returns:
            Dict containing the mandate details
        """
        if not isinstance(mandate_id, str):
            raise ValueError("mandate_id must be a string")
            
        try:
            mandate = self.gocardless_pro_client.mandates.get(mandate_id)
            return mandate
        except Exception as e:
            print(f"Error retrieving mandate: {str(e)}")
            return None