# SMS Testing
## 1. Set up MockSMS
First, you’ll need to run **MockSMS** as a local service using Docker. MockSMS will act as a fake SMS gateway, allowing you to capture and review SMS messages.

**Steps to Run MockSMS:**
```bash
# Pull the MockSMS Docker image
docker pull smsslabs/mocksms

# Run MockSMS Docker container
docker run -p 1080:1080 -p 1025:1025 smsslabs/mocksms
```
- **Port 1080** will expose the web interface where you can view the captured SMS.
- **Port 1025** will expose the SMTP-like interface for capturing SMS.
This setup will allow you to capture any SMS messages sent during testing in your local environment.

## 2. Mock AWS SNS with LocalStack
You can use **LocalStack**, a tool that mocks AWS services, including **SNS**, in combination with **MockSMS** to simulate the sending of SMS messages without actually using AWS infrastructure.

**Steps to Run LocalStack:**
```bash
# Pull and run the LocalStack Docker image
docker pull localstack/localstack

# Run LocalStack container
docker run -p 4566:4566 -p 4571:4571 localstack/localstack
```
- **Port 4566** is where all the AWS services (including SNS) will be available locally.
- With LocalStack, you can simulate SNS and use it to send mock SMS messages to MockSMS.
## 3. Configure Boto3 to Use LocalStack
In your Python project, configure **Boto3** to connect to LocalStack’s SNS instead of the real AWS SNS service. This way, you’ll be able to simulate sending SMS messages.

**Boto3 Configuration for LocalStack:**
```python
import boto3

# Create a boto3 client configured to use LocalStack SNS
sns_client = boto3.client(
    'sns',
    region_name='us-east-1',  # Use any AWS region
    endpoint_url='http://localhost:4566',  # LocalStack endpoint
    aws_access_key_id='fakeAccessKey',
    aws_secret_access_key='fakeSecretKey'
)

# Create an SNS topic in LocalStack
response = sns_client.create_topic(Name='test_sms_topic')
topic_arn = response['TopicArn']

# Subscribe a phone number to the topic
sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol='sms',
    Endpoint='+1234567890'  # Mock phone number
)

# Publish a message to the topic (This will be captured by MockSMS)
sns_client.publish(
    TopicArn=topic_arn,
    Message='This is a test message from MockSMS',
    PhoneNumber='+1234567890'  # Mock phone number
)
```
This configuration will direct SMS messages to **LocalStack**, which will simulate AWS SNS behavior, without connecting to real AWS infrastructure.

## 4. Viewing Captured SMS in MockSMS
Once your Boto3 client is configured to use LocalStack, and you’ve set up MockSMS, any SMS message that would normally be sent via AWS SNS will now be captured by MockSMS.

To view the captured SMS:

- Open your browser and go to `http://localhost:1080`.
- You will see a list of captured SMS messages in the MockSMS web interface.
## 5. Running MockSMS and LocalStack in CI (Docker-Compose)
In a CI/CD pipeline, you can run **MockSMS** and **LocalStack** together using `docker-compose`. Here’s an example `docker-compose.yml` file that sets up both services:

```yaml
version: '3'
services:
  mocksms:
    image: smsslabs/mocksms
    ports:
      - "1080:1080"
      - "1025:1025"
  
  localstack:
    image: localstack/localstack
    environment:
      - SERVICES=sns
      - DEBUG=1
    ports:
      - "4566:4566"  # LocalStack services
      - "4571:4571"
```
In your CI pipeline (e.g., GitHub Actions, GitLab CI), you can spin up these services as part of your test setup, allowing for full simulation of the SMS functionality.

## 6. Testing in Python (Unit Test Example)
Here’s a simple unit test example that verifies the integration:

```python
import unittest
from unittest.mock import patch
import boto3

class TestSMSNotification(unittest.TestCase):

    @patch('boto3.client')
    def test_send_sms(self, mock_boto_client):
        # Mock Boto3 SNS client
        sns_client = mock_boto_client.return_value
        
        # Call function to send SMS
        sns_client.publish.return_value = {"MessageId": "mocked-message-id"}
        
        # Call function to simulate sending an SMS
        response = sns_client.publish(
            TopicArn="arn:aws:sns:us-east-1:123456789012:test_sms_topic",
            Message="Test message",
            PhoneNumber="+1234567890"
        )
        
        # Assert the publish method was called and returned a valid MessageId
        sns_client.publish.assert_called_once()
        self.assertEqual(response["MessageId"], "mocked-message-id")

if __name__ == '__main__':
    unittest.main()
```
This test uses `unittest.mock` to patch the Boto3 SNS client and simulate the behavior. You can run it in your CI pipeline with **MockSMS** and **LocalStack** running in the background.

## Conclusion
By using **MockSMS** for capturing SMS and **LocalStack** for mocking AWS SNS, you can create a complete local and CI environment for testing SMS functionality in your Python project. The combination of these tools will allow you to thoroughly test SMS logic without needing to send real messages or interact with live AWS resources.