# Storage Testing

## Install MinIO Server
This is the simplest way to get MinIO up and running.

1. Pull the MinIO Docker image:
```bash
Copia el codi
docker pull minio/minio
```

2. Run the MinIO container:
```bash
docker run -p 9000:9000 -p 9001:9001 --name minio-server \
-e "MINIO_ROOT_USER=minioadmin" \
-e "MINIO_ROOT_PASSWORD=minioadmin" \
minio/minio server /data --console-address ":9001"
```
This command:
- Maps port `9000` for S3 API access and `9001` for the web console.
- Sets the MinIO root credentials (`MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD`).


## Configure Your Application to Use MinIO
To use MinIO as an S3 mock, your application needs to point to the MinIO server instead of AWS. You can configure your app to interact with MinIO by providing the necessary S3 credentials and endpoint.

Example: Using MinIO with AWS SDK in Python (Boto3)
1. Install Boto3 if you're using Python:

```bash
pip install boto3
```
2. Configure Boto3 to use MinIO:
```python
import boto3

s3 = boto3.resource(
    's3',
    endpoint_url='http://localhost:9000',  # MinIO server
    aws_access_key_id='minioadmin',        # MinIO access key
    aws_secret_access_key='minioadmin',    # MinIO secret key
    region_name='us-east-1',               # S3 region
)
```
