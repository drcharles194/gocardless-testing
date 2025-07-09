from homework.main import GoCardlessPartner
from homework.gocardless_operations import GoCardlessOperations
import os

def run_flow():
    # Step 1: Authenticate partner (if needed)
    print("Step 1: Partner Authentication")
    partner = GoCardlessPartner()
    
    if not os.environ.get('PARTNER_TOKEN'):
        partner.authenticate_partner()
    else:
        print("Proceeding")
    
    # Step 2: Create operations instance
    operations = GoCardlessOperations(partner)
    
    # Step 3: Create Billing Request Flow
    print("\nStep 2: Creating Billing Request Flow")
    amount = int(input("Enter payment amount in pence (e.g., 1000 for £10.00): "))
    description = input("Enter payment description: ")
    
    flow = operations.create_billing_request_and_flow(
        amount=amount,
        currency="GBP",
        description=description
    )
    
    # Print the authorization URL for the customer
    print("\nPlease share this URL with your customer to complete the payment:")
    print(flow.authorisation_url)
    
    # Step 4: Check flow status and get mandate details
    if input("\nWould you like to check the flow status and mandate details? (y/n): ").lower() == 'y':
        # First get the billing request to retrieve the mandate ID
        billing_request = operations.get_billing_request()
        if billing_request:
            print("\nBilling Request Details:")
            print(f"ID: {billing_request.id}")
            print(f"Status: {billing_request.status}")
            
            # Now get the mandate details if we have a mandate ID
            if operations.mandate_id:
                mandate = operations.get_mandate(operations.mandate_id)
                if mandate:
                    print("\nMandate Details:")
                    print(f"ID: {mandate.id}")
                    print(f"Status: {mandate.status}")
                    print(f"Reference: {mandate.reference}")
                    print(f"Created at: {mandate.created_at}")
                    print(f"Scheme: {mandate.scheme}")
                else:
                    print("\nCould not retrieve mandate details. The customer may still be completing the flow.")
            else:
                print("\nNo mandate ID available yet. The customer may still be completing the flow.")
        else:
            print("\nCould not retrieve billing request details.")

if __name__ == "__main__":
    run_flow() 