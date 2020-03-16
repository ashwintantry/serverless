import os
import sys
import fnmatch
import re
import boto3
from common import execute

AWS_ACCOUNT_ID = os.environ['AWS_ACCOUNT_ID']
INFRA_ACTION = os.environ['INFRA_ACTION']
AWS_ACCESS_KEY_ID1 = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY1 = os.environ['AWS_SECRET_ACCESS_KEY']

if __name__ == "__main__":
    try:
        #credentials = get_temporary_credentials("AssumeRoleSessionWOW")

        aug_env = os.environ.copy()
        aug_env['TF_VAR_account_id'] = AWS_ACCOUNT_ID

        print("=== Terraform %s ===" % (INFRA_ACTION))
        #os.chdir('../infra/terraform')
        print(os.getcwd())
        execute(['make', INFRA_ACTION], stdout=sys.stdout, stderr=sys.stderr, env=aug_env)

    except:
        raise Exception('`IaC` phase failed!')
