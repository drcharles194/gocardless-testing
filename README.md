# GoCardless Testing Integration

A Python implementation for integrating with the GoCardless API using their modern Billing Request Flow. This project demonstrates partner authentication, billing request creation, and mandate management for Direct Debit payments.

## Overview

This project provides a command-line interface for testing GoCardless API integration, specifically focusing on:
- Partner authentication (OAuth2 or token-based)
- Creating billing requests with payment details
- Generating customer authorization URLs
- Retrieving and managing mandates
- Working with both sandbox and production environments

## Features

- ✅ **Flexible Authentication**: Supports both OAuth2 flow and direct token authentication
- ✅ **Billing Request Flow**: Modern approach to collecting mandates and payments
- ✅ **CLI Interface**: Easy-to-use command-line tool for testing
- ✅ **Environment Configuration**: Secure handling of API credentials
- ✅ **Sandbox Support**: Safe testing environment
- ✅ **Mandate Management**: Retrieve and display mandate details

## Project Structure

```
gocardless-testing/
├── homework/
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # Command-line interface
│   ├── main.py                  # Core GoCardless client implementation
│   └── gocardless_operations.py # Business logic for API operations
├── tests/
│   └── __init__.py              # Test package
├── .env                         # Environment variables (local only)
├── .gitignore                   # Git ignore rules
├── LICENSE                      # GNU GPL v2.0 license
├── README.md                    # This file
├── poetry.lock                  # Locked dependencies
└── pyproject.toml              # Project configuration and dependencies
```

## Prerequisites

- **Python 3.9+**: Required for the application
- **Poetry**: For dependency management
- **GoCardless Account**: Partner account with API access
- **API Credentials**: Either OAuth credentials or Partner token

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/drcharles194/gocardless-testing.git
   cd gocardless-testing
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Set up environment variables:**
   
   Create a `.env` file in the project root:
   ```env
   # For OAuth authentication (choose this OR token-based)
   GOCARD_CLIENT_ID=your_client_id
   GOCARD_SECRET=your_client_secret
   
   # For token-based authentication (choose this OR OAuth)
   PARTNER_TOKEN=your_partner_token
   PARTNER_ORG_ID=your_organisation_id
   ```

## Usage

### Running the CLI

Execute the main script using Poetry:

```bash
poetry run python -m homework.cli
```

### Example Workflow

1. **Start the application:**
   ```bash
   poetry run python -m homework.cli
   ```

2. **Authentication:**
   - If using OAuth: Follow the prompted URL and complete the authorization
   - If using token: Authentication happens automatically

3. **Create billing request:**
   - Enter payment amount in pence (e.g., `1000` for £10.00)
   - Provide a payment description

4. **Customer flow:**
   - Share the generated authorization URL with your customer
   - Customer completes mandate setup and payment authorization

5. **Check results:**
   - Use the CLI option to check billing request status
   - View mandate details once created

### Sample Output

```
Step 1: Partner Authentication
Using existing partner token from environment

Step 2: Creating Billing Request Flow
Enter payment amount in pence (e.g., 1000 for £10.00): 1500
Enter payment description: Test payment for integration

Please share this URL with your customer to complete the payment:
https://pay-sandbox.gocardless.com/billing-request-flows/BRF123...

Would you like to check the flow status and mandate details? (y/n): y

Billing Request Details:
ID: BR123456789
Status: pending_submission

Mandate Details:
ID: MD123456789
Status: pending_submission
Reference: REF123456789
Created at: 2024-01-15T10:30:00.000Z
Scheme: bacs
```

## Development

### Dependencies

The project uses the following key dependencies:

- **gocardless-pro**: Official GoCardless Pro Python client
- **requests-oauthlib**: OAuth2 authentication support
- **python-dotenv**: Environment variable management

### Environment Configuration

- **Sandbox**: The project uses GoCardless sandbox by default for safe testing
- **Production**: To switch to production, modify the `environment` parameter in the client initialization

### Running Tests

```bash
poetry run pytest
```

## API Reference

This project integrates with the following GoCardless API endpoints:

- **Billing Requests**: Create and manage billing requests
- **Billing Request Flows**: Generate customer authorization flows
- **Mandates**: Retrieve mandate details and status

For full API documentation, visit: [GoCardless API Documentation](https://developer.gocardless.com/api-reference)

## Security Notes

- ⚠️ **Never commit** your `.env` file or API credentials to version control
- 🔒 **Use sandbox** environment for testing and development
- 🛡️ **Rotate tokens** regularly in production environments
- 📋 **Review permissions** when setting up OAuth applications

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues related to:
- **GoCardless API**: Check the [official documentation](https://developer.gocardless.com/)
- **This integration**: Open an issue in this repository
- **General questions**: Review the API documentation or contact GoCardless support

---

**Note**: This is a testing and demonstration project. For production use, ensure you follow GoCardless's security guidelines and implement proper error handling, logging, and monitoring.
