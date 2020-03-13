#!groovy

pipeline {
    agent any
    environment {
          INFRA_ACTION = "apply"
         }
    stages {
        stage('Setup') {
            steps {
                    sh 'python3 -m venv venv'
                    sh 'venv/bin/pip3 install -r requirements.txt'
            }
        }
        stage('Infrastructure Creation') {
            steps {
                   script {
                           sh 'AWS_ACCOUNT_ID=763453301580 venv/bin/python3 infra.py'
                        }
            }
        }
        stage('Deploy') {
            steps {
                    script {
                        if (env.INFRA_ACTION == 'apply')
                           sh 'AWS_ACCOUNT_ID=763453301580 venv/bin/python3 deploy.py'
                        }
            }
        }
    }
}
