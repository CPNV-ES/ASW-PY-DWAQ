from botocore.config import Config

aws = {
    "aws_service_name": "ec2",
    "config": Config(
        region_name="",
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    ),
    "aws_access_key_id": "",
    "aws_secret_access_key": "",
}