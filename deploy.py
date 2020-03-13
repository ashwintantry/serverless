import os
import sys
import json
import fnmatch
import re
import boto3
from common import execute
# from notify import info_message, error_message, success_message

AWS_ACCOUNT_ID = os.environ['AWS_ACCOUNT_ID']
INFRA_ACTION = os.environ['INFRA_ACTION']
#LAYER = os.environ['LAYER']
# SLACK_TITLE = "WOW-Serverless-%s-Pipeline" % LAYER
#FILE_PATH = os.environ.get('FILE_PATH', None)

if __name__ == "__main__":
    try:

        aug_env = os.environ.copy()
        aug_env['TF_VAR_account_id'] = AWS_ACCOUNT_ID
        owd = os.getcwd()
        execute(['make', 'init'], env=aug_env, stdout=sys.stdout, stderr=sys.stderr)
        bucket_name = execute(['terraform', 'output', '-json', 's3_bucket_name'], env=aug_env).strip()
        print('s3_bucket_name:', bucket_name)
        api_http = execute(['terraform', 'output', '-json', 'api_http'], env=aug_env).strip()
        print('api_http:', api_http)
        pool_id = execute(['terraform', 'output', '-json', 'pool_id'], env=aug_env).strip()
        print('pool_id:', pool_id)
        client_id = execute(['terraform', 'output', '-json', 'client_id'], env=aug_env).strip()
        print('s3_bucket_name:', client_id)
        print(os.getcwd())
        os.chdir("website/js")
        print(os.getcwd())
        with open('config.js', 'r') as f:    
            lines = f.readlines()
        with open('config.js', 'w') as f:
            for line in lines:
                line = line.replace('temp_userPoolId', pool_id)
                line = line.replace('temp_userPoolClientId', client_id)
                line = line.replace('temp_invokeUrl', api_http)
                f.write(line)
        with open('config.js', 'r') as f:    
            print(f.readlines())
        os.chdir("../")
        s3 = boto3.client('s3')
        print("Current dir : " + os.getcwd())
        for root, dirs, files in os.walk(os.getcwd()):

            for filename in files:
                # construct the full local path
                local_path = os.path.join(root, filename)
                with open(local_path) as f:
                    s = f.read()
                    print("File: "+local_path)
                    s3.upload_file(local_path,''s3://tan3-test-serverless/'',s)

                #print("File: "+local_path)
                #s3.upload_file(local_path, bucket_name)
        # get file to deploy from the build execution if we haven't been passed pre-built path as an env var
        #if FILE_PATH is None:
            #for file in os.listdir('../target/'):
                #if fnmatch.fnmatch(file, "tabledata*.jar"):
                    #file_to_deploy = file

            #if not file_to_deploy:
                #raise Exception('File to deploy not found')
        # else copy file from FILE_PATH to the ../target directory and set that as file_to_deploy
        #else:
            #target_dir = '../target'
            #if not os.path.exists(target_dir):
                #os.makedirs(target_dir)
            #file_to_deploy = os.path.basename(FILE_PATH)
            #execute(['cp', FILE_PATH, "%s/%s" % (target_dir, file_to_deploy)])

        #aug_env['TF_VAR_lambda_payload_filename'] = "../../../../target/%s" % file_to_deploy

        #print("=== Terraform %s for %s ===" % (INFRA_ACTION, LAYER))
        #os.chdir('../infra/terraform')
        #print(os.getcwd())
        #execute(['make', INFRA_ACTION], stdout=sys.stdout, stderr=sys.stderr, env=aug_env)

    except:
        raise Exception('`IaC` phase failed!')
