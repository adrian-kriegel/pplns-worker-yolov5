
import boto3
from util import env
import urllib.parse

class S3UrlSigner:

  def __init__(self):

    self.s3 = boto3.client(
      's3',
      aws_access_key_id=env('AWS_S3_ACCESS_KEY_ID'),
      aws_secret_access_key=env('AWS_S3_SECRET_ACCESS_KEY'),
      region_name=env('AWS_S3_REGION'),
    )

  def __call__(self, s3url : str) -> str:

    parsed = urllib.parse.urlparse(s3url)

    return self.s3.generate_presigned_url(
      'get_object',
      Params={
        'Bucket': parsed.netloc.split('.')[0],
        'Key': parsed.path[1:]
      },
      ExpiresIn=100000
    )
