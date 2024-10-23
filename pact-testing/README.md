
## Steps to Integrate Pact Broker with `pytest` and `pact-python`:
1. **Install Dependencies:** If you haven't already installed the dependencies, ensure you have pact-python installed:

```bash
pip install pact-python pytest requests
```
2. **Define Environment Variables:** You can define your Pact Broker credentials and URL using environment variables (for security reasons) or directly in the code.

For example:

```bash
export PACT_BROKER_URL=http://your-pact-broker-url
export PACT_BROKER_USERNAME=your-username
export PACT_BROKER_PASSWORD=your-password
```
3. **Publishing Contracts to the Pact Broker:** After your tests have run and the contract is verified, you can publish the contracts to the Pact Broker. The `pact-python` library supports this with the `publish_to_broker` method.

4. **`Pytest` Fixture for Broker Integration:**

Here's how you can modify the previous example to include the Pact Broker:

```python
import pytest
from pact import Consumer, Provider
import os
import requests

PACT_MOCK_HOST = 'localhost'
PACT_MOCK_PORT = 1234

PACT_BROKER_URL = os.getenv('PACT_BROKER_URL', 'http://your-pact-broker-url')
PACT_BROKER_USERNAME = os.getenv('PACT_BROKER_USERNAME', None)
PACT_BROKER_PASSWORD = os.getenv('PACT_BROKER_PASSWORD', None)
PACT_CONSUMER_VERSION = '1.0.0'  # Use your app version or CI build number


# Pact pytest fixture
@pytest.fixture(scope='session')
def pact():
    # Setup Pact between a consumer and a provider
    pact = Consumer('ConsumerService').has_pact_with(Provider('ProviderService'),
                                                     host_name=PACT_MOCK_HOST,
                                                     port=PACT_MOCK_PORT)

    # Start the mock service
    pact.start_service()

    yield pact

    # Stop the service and verify the interactions
    pact.stop_service()
    pact.verify()

    # Publish the contract to the Pact Broker after the tests have run
    pact.publish_to_broker(
        broker_base_url=PACT_BROKER_URL,
        consumer_version=PACT_CONSUMER_VERSION,
        broker_username=PACT_BROKER_USERNAME,
        broker_password=PACT_BROKER_PASSWORD,
        tags=['test', 'latest']
    )


def test_get_user(pact):
    # Define the expected interaction
    expected = {
        'id': 123,
        'name': 'John Doe',
        'email': 'johndoe@example.com'
    }

    # Setting up an interaction
    pact.given('User with ID 123 exists') \
        .upon_receiving('a request for user with ID 123') \
        .with_request('GET', '/users/123') \
        .will_respond_with(200, body=expected)

    # Execute the interaction
    with pact:
        result = requests.get(f'http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}/users/123')

    # Assert the response from the provider matches what was expected
    assert result.status_code == 200
    assert result.json() == expected
```
## Breakdown of Code for Pact Broker Integration:
1. **Environment Variables:**

`PACT_BROKER_URL`, `PACT_BROKER_USERNAME`, and `PACT_BROKER_PASSWORD` are read from environment variables, which store the URL and credentials for your Pact Broker.

2. **Publishing the Pact:**

- `pact.publish_to_broker()` is called after the Pact verification to push the contract to the broker.
- The parameters include:
  - `broker_base_url`: The Pact Broker's URL.
  - `consumer_version`: The version of your consumer (e.g., 1.0.0, or ideally, your CI build version).
  - `broker_username` and `broker_password`: For authenticated access to the broker.
  - `tags`: A list of tags you want to associate with this contract (e.g., test, latest, etc.).

3. **Versioning:**

- **Consumer Version:** The version is important when publishing pacts to the broker, as it helps track which version of your consumer service generated the pact.
- Typically, you would use your CI build number or release version.

## Running the Tests and Publishing the Pact:
1. Run your tests as usual:

```bash
pytest
```
2. Once the tests are completed and successful, the pact file will be published to your Pact Broker, where the provider team can later verify it.

## Retrieving Pacts from the Broker (for Provider Tests):
For **provider-side** tests, you would typically retrieve the pacts from the broker and verify them against your provider implementation. This would require adding additional configuration in your provider tests to download the pacts and validate them.

Here’s a very basic example for retrieving and verifying a pact from the broker:

```python
import os
from pact import Verifier
import pytest
import subprocess

PACT_BROKER_URL = os.getenv('PACT_BROKER_URL', 'http://your-pact-broker-url')
PACT_BROKER_USERNAME = os.getenv('PACT_BROKER_USERNAME', None)
PACT_BROKER_PASSWORD = os.getenv('PACT_BROKER_PASSWORD', None)
PACT_PROVIDER_VERSION = '1.0.0'  # This could be your app version or CI build number
PROVIDER_BASE_URL = 'http://localhost:5000'  # Replace with your provider's actual URL

# Fixture to start the provider (mock or real server)
@pytest.fixture(scope='session')
def start_provider():
    """Start the provider service and ensure it is running before tests."""
    # Example of starting a Flask app (or any other provider service)
    print("Starting provider service...")
    process = subprocess.Popen(['flask', 'run'], stdout=subprocess.PIPE)

    # Wait for the server to start
    yield

    # Teardown - stop the provider after the tests
    print("Stopping provider service...")
    process.terminate()
    process.wait()


# Provider test to verify contracts against the Pact Broker
def test_provider_against_pact_broker(start_provider):
    """Verify the provider service against the Pact Broker contracts."""
    # At this point, the provider service is assumed to be running due to the fixture
    verifier = Verifier(provider="ProviderService")

    # Verify the provider against all pacts for this provider available in the broker
    success = verifier.verify_with_broker(
        broker_url=PACT_BROKER_URL,
        broker_username=PACT_BROKER_USERNAME,
        broker_password=PACT_BROKER_PASSWORD,
        provider_base_url=PROVIDER_BASE_URL,
        publish_version=PACT_PROVIDER_VERSION,
        provider_branch="main",  # Optional: If you're using version branches in Pact Broker
        provider_tags=["dev"],  # Tags that indicate which consumer pacts to verify
        enable_pending=True,  # Optional: If you use pending pacts in Pact Broker
    )

    # Ensure the verification passed
    assert success == 0, "Pact verification failed"

```
In this case, the `Verifier` fetches the pact from the broker and verifies it against your running provider instance.