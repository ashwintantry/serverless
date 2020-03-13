#!groovy

pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                    sh 'python3 -m venv venv'
                    sh 'venv/bin/pip3 install -r requirements.txt'
            }
        }
        stage('Infrastructure Creation') {
            environment {
                INFRA_ACTION = "destroy"
            }
            steps {
                        script {
                                sh 'AWS_ACCOUNT_ID=763453301580 venv/bin/python3 infra.py'
                        
                }
            }
        }

    }
}
