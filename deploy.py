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


if __name__ == "__main__":
    try:

        aug_env = os.environ.copy()
        aug_env['TF_VAR_account_id'] = AWS_ACCOUNT_ID
        aug_env['AWS_ACCESS_KEY_ID'] = credentials['genAccessKey']
        aug_env['AWS_SECRET_ACCESS_KEY'] = credentials['genSecretAccessKey']
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
        s3 = boto3.client('s3',
                          aws_access_key_id=aug_env['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=aug_env['AWS_SECRET_ACCESS_KEY'])
        print("Current dir : " + os.getcwd())
        for root, dirs, files in os.walk(os.getcwd()):
            for filename in files:
                local_path = os.path.join(root, filename)
                #with open(local_path) as f:
                    #s = f.read()
                    #print("File: "+local_path)
                    #s3.upload_file(local_path,"tan3-test-serverless",filename)
                    

                print("File: "+local_path)
                if fnmatch.fnmatch(local_path, "*/css/*"):
                    file_path_temp = "css/"+filename
                    print (file_path_temp)
                elif fnmatch.fnmatch(local_path, "*/fonts/*"):
                    file_path_temp = "fonts/"+filename
                    print (file_path_temp)
                elif fnmatch.fnmatch(local_path, "*/images/*"):
                    file_path_temp = "images/"+filename
                    print (file_path_temp)
                elif fnmatch.fnmatch(local_path, "*/js/vendor/*"):
                    file_path_temp = "js/vendor/"+filename
                    print (file_path_temp)
                elif fnmatch.fnmatch(local_path, "*/js/*"):
                    file_path_temp = "js/"+filename
                    print (file_path_temp)
                else: file_path_temp =filename
                if fnmatch.fnmatch(local_path, "*.gif"):
                    s3.upload_file(local_path,"tan3-test-serverless",file_path_temp,ExtraArgs={'ContentType': "image/gif"})
                elif fnmatch.fnmatch(local_path, "*.png"):
                    s3.upload_file(local_path,"tan3-test-serverless",file_path_temp,ExtraArgs={'ContentType': "image/png"})
                elif fnmatch.fnmatch(local_path, "*.ico"):
                    s3.upload_file(local_path,"tan3-test-serverless",file_path_temp)
                elif fnmatch.fnmatch(local_path, "*.html"):
                    s3.upload_file(local_path,"tan3-test-serverless",file_path_temp,ExtraArgs={'ContentType': "text/html"})
                elif fnmatch.fnmatch(local_path, "*.css"):
                    s3.upload_file(local_path,"tan3-test-serverless",file_path_temp,ExtraArgs={'ContentType': "text/css"})
                elif fnmatch.fnmatch(local_path, "*.js"):
                    s3.upload_file(local_path,"tan3-test-serverless",file_path_temp,ExtraArgs={'ContentType': "text/js"})
                else: s3.upload_file(local_path,"tan3-test-serverless",file_path_temp,ExtraArgs={'ContentType': "text/plain"})
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
