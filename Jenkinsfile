pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git url:'https://github.com/prolegion2021/shadowapp.git', branch: 'main'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t shadowapp:latest .'
            }
        }
        stage('Test') {
            steps {
                sh 'ls'
                sh 'cd shadow-app'
                sh 'ls'
                sh 'docker run -t shadowapp:latest python shadow-app/unit_test.py'
            }
        }
        stage('Create Image') {
            steps {
                sh 'docker build -t prolegion/shadowapp:latest -f Dockerfile .'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: '8bb8de30-cd61-4c56-9e1b-9732b5412764', usernameVariable: 'DOCKER_HUB_USERNAME', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                    sh 'docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD'
                    sh 'docker push prolegion/shadowapp:latest'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 5000:5000 prolegion/shadowapp:latest'
                sh 'docker ps'
                sh 'docker stop $(docker ps -q --filter ancestor=prolegion/shadowapp:latest)'
            }
        }
    }
}
