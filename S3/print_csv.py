import boto3
from smart_open import open


def print_csv(path_to_file):
    session_s3 = boto3.Session(
        aws_access_key_id='q3dEt2FODkSFF3AeM3_w',
        aws_secret_access_key='BnLcTZbcI7g9brLmGpT3JiLhQD0ouUHkkoHikL85',
        region_name='us-east-1')
    client_s3 = session_s3.client('s3', endpoint_url='https://storage.yandexcloud.net')
    Bucket = 'rosstat-storage'
    with open(f's3://{Bucket}/{path_to_file}', 'r', transport_params={'client': client_s3}) as csv_f:
        for row in csv_f:
            print(row)


print_csv('reports/identified/2019-01-27/identified')