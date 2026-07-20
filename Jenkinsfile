pipeline {
    agent any

    stages {

        stage('Verify Environment') {
            steps {
                echo '=== Jenkins Environment ==='

                sh 'whoami'
                sh 'pwd'

                sh 'git --version'
                sh 'python3 --version'
                sh 'docker --version'
            }
        }

    }
}