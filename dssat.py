import os
import requests
import boto3
from botocore.exceptions import ClientError
import json
import logging
from datetime import datetime

s3 = boto3.client('s3')

os.chdir('/tmp/')


def lambda_handler(event, context):

    body = json.loads(event['body'])
    input_json = body       

    r = requests.get(input_json['file_url'], allow_redirects=True)
    open(input_json['file_name'], 'wb').write(r.content)    
    init_files = os.listdir()
    os.system('/var/task/DSSAT47/dscsm047 A ' + input_json['file_name'] + ' > command_line_output.txt')
    

    all_files = os.listdir()
    output_files = [x for x in all_files if x not in init_files]

    dt_string = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    dt_string = dt_string.replace('/','_')
    dt_string = dt_string.replace(' ','_')
    dt_string = dt_string.replace(':','_')
    

    files_list = []
    for file in output_files:
        target_bucket = 'lambda-dssat'

        object_name = input_json['file_name'].replace('.','_') + '_' + dt_string + '/' + file
        
        # Upload file to S3
        try:
            response = s3.upload_file(file, target_bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return {
                'statusCode': 500,
                'body': json.dumps(e)
            }

        files_list.append('https://lambda-dssat.s3.eu-central-1.amazonaws.com/' + object_name)
        os.remove(file)

    my_output = {
        'files_list': files_list
    }

    return {
        'statusCode': 200,
        'body': json.dumps(my_output)
    }

