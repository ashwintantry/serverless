import os
import sys
import fnmatch
import re
import boto3
#from assume_role import get_temporary_credentials
from common import execute
# from notify import info_message, error_message, success_message

AWS_ACCOUNT_ID = os.environ['AWS_ACCOUNT_ID']
INFRA_ACTION = os.environ['INFRA_ACTION']
#LAYER = os.environ['LAYER']
# SLACK_TITLE = "WOW-Serverless-%s-Pipeline" % LAYER
#FILE_PATH = os.environ.get('FILE_PATH', None)

if __name__ == "__main__":
    try:
        #credentials = get_temporary_credentials("AssumeRoleSessionWOW")

        aug_env = os.environ.copy()
        #aug_env['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
        #aug_env['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
        #aug_env['AWS_SESSION_TOKEN'] = credentials['SessionToken']
        aug_env['TF_VAR_account_id'] = AWS_ACCOUNT_ID

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

        print("=== Terraform %s for %s ===" % (INFRA_ACTION, LAYER))
        #os.chdir('../infra/terraform')
        print(os.getcwd())
        execute(['make', INFRA_ACTION], stdout=sys.stdout, stderr=sys.stderr, env=aug_env)

    except:
        raise Exception('`IaC` phase failed!')