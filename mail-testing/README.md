# MailPit
## Main Features
1. **Easy Setup and Usage:** Mailpit is designed to be lightweight and easy to set up, making it ideal for developers who need a simple tool for email testing. It doesn't require heavy configuration or dependencies, which allows for quick integration into development environments.
2. **Local SMTP Server:** Mailpit acts as a local SMTP server, allowing developers to intercept outgoing emails without sending them to real recipients. This is helpful for testing the content, formatting, and other aspects of the emails during development without spamming users.
3. **Web UI for Email Review:** Mailpit provides a web-based interface to view all captured emails. It allows developers to easily browse, search, and review the emails sent during the testing phase, ensuring that emails are formatted correctly and contain the right content.
4. **Supports HTML, Plain Text, and Attachments:** Mailpit captures emails in different formats (HTML, plain text) and also supports attachments, making it versatile for testing complex emails.
5. **Email Search and Filtering:** Mailpit’s web UI includes search and filtering options that allow you to find specific emails, which is particularly useful in large projects where multiple emails might be sent during testing.
6. **Cross-platform Compatibility:** It is cross-platform, running on Linux, macOS, and Windows, making it accessible regardless of the development environment.
7. **REST API for Automation:** Mailpit offers a REST API, which makes it easy to integrate email testing into CI/CD pipelines or other automated testing environments. You can programmatically check if the right emails were sent, verify their content, and even run tests on those emails.
8. **Secure and Isolated Testing:** Since Mailpit captures emails locally, it provides a secure environment where sensitive data in emails can be tested without exposing it to the internet or real users.

## Implement Mailpit for Email Testing
### Install Mailpit
You can install Mailpit on your local development machine or within a Docker container.

1. Pull the latest Mailpit image from Docker Hub:
```bash
docker pull axllent/mailpit
```
2. Run Mailpit in a Docker container:
```bash
docker run -p 1025:1025 -p 8025:8025 axllent/mailpit
```
This will expose the SMTP server on port 1025 and the web UI on port 8025.
### Configure Your Application's SMTP Settings
To start capturing emails, you need to configure your application to use Mailpit as the SMTP server. Set the SMTP host and port to point to Mailpit:

```yaml
SMTP_HOST: "localhost"
SMTP_PORT: 1025
```
Alternatively, if using Docker, the host might depend on your Docker network settings (e.g., use the container name as the hostname).

### Integration with CI/CD (Optional)
You can run Mailpit as part of your CI/CD pipeline to test email functionality. Use Docker to start Mailpit in your pipeline, configure the SMTP settings in your tests, and then use the REST API to verify emails were sent and contain the correct information.

Example in a CI pipeline:

```yaml
stages:
  - test

test_email_functionality:
  stage: test
  services:
    - name: axllent/mailpit
      alias: mailpit
  script:
    - ./run_tests.sh
    - curl http://mailpit:8025/api/v1/messages  # Fetch email data
```