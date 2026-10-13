pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Pulls the latest code from GitHub
                checkout scm
            }
        }
        stage('Build Environment') {
            steps {
                echo 'Building ACEest Application Environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Test Pipeline') {
            steps {
                echo 'Running Pytest Validation...'
                sh '''
                    . venv/bin/activate
                    pytest tests/
                '''
            }
        }
    }
}