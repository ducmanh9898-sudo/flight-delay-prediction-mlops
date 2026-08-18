pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            environment {
                OTEL_SDK_DISABLED = 'true'
            }

            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                      -t flight-delay-api:${BUILD_NUMBER} .
                '''
            }
        }
    }
}