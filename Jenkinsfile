pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building ACEest Application...'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                echo 'Running Pytest...'
                sh 'pytest tests/'
            }
        }
    }
}
