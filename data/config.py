import logging

logging.basicConfig(level=logging.INFO)

RABBIT_MQ_URL = "amqp://rmuser:rmpassword@rabbitmq:5672/"

S3_ACCESS_KEY = 'minioadmin'
S3_SECRET_KEY = 'minioadmin'
S3_BUCKET = 'smart-dictophone-audio'
S3_ENDPOINT = "minio:9000"
S3_SECURE = False
S3_REGION = 'us-east-1'

BUSINESS_LOGIC_SERVICE = 'http://api:8888'
BUSINESS_LOGIC_API_KEY = 'test-api-key'
