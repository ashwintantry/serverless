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
                withCredentials([string(credentialsId:'genAccessKey',variable:'AWS_ACCESS_KEY_ID'),
                    string(credentialsId:'genSecretAccessKey',variable:'AWS_SECRET_ACCESS_KEY')]) {
                   script {
                       //if (env.INFRA_ACTION == 'destroy')
                           sh 'AWS_ACCOUNT_ID=868707139949 venv/bin/python3 infra.py'
                        }
                }
            }
        }
        stage('Deploy') {
            steps {
                withCredentials([string(credentialsId:'genAccessKey',variable:'AWS_ACCESS_KEY_ID'),
                    string(credentialsId:'genSecretAccessKey',variable:'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        if (env.INFRA_ACTION == 'apply')
                           sh 'AWS_ACCOUNT_ID=868707139949 venv/bin/python3 deploy.py'
                        }
                }
            }
        }
    }
}
