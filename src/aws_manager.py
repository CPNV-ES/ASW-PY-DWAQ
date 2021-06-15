import boto3
import aws_config as cfg


class AwsManager:
    def __init__(self):
        self._client = boto3.client(
            cfg.aws["aws_service_name"],
            config=cfg.aws["config"],
            aws_access_key_id=cfg.aws["aws_access_key_id"],
            aws_secret_access_key=cfg.aws["aws_secret_access_key"],
            use_ssl=False,
        )
        self._resource = boto3.resource(
            cfg.aws["aws_service_name"],
            config=cfg.aws["config"],
            aws_access_key_id=cfg.aws["aws_access_key_id"],
            aws_secret_access_key=cfg.aws["aws_secret_access_key"],
            use_ssl=False,
        )
