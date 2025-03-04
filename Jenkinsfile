pipeline {
    agent any
    
    environment {
        DOCKER_HUB_TOKEN = credentials('docker-hub-token')
        APP_NAME = 'mlops-a01'
        DOCKER_IMAGE = "ahmed93560/${APP_NAME}"
        DOCKER_USERNAME = 'ahmed93560'
        ADMIN_EMAIL = 'khanahmed6965@gmail.com'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                bat "docker build -t ${DOCKER_IMAGE} ."
            }
        }
        
        stage('Tag Docker Image') {
            steps {
                bat "docker tag ${DOCKER_IMAGE} ${DOCKER_USERNAME}/${APP_NAME}:latest"
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
                    bat 'docker push ${DOCKER_IMAGE} ${DOCKER_USERNAME}/${APP_NAME}:latest'
                }
            }
        }
    }
    
    post {
        success {
            emailext (
                subject: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>
                <p>The Docker image ${DOCKER_IMAGE} has been successfully built and pushed to Docker Hub.</p>""",
                to: "${ADMIN_EMAIL}",
                mimeType: 'text/html'
            )
        }
        failure {
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
                to: "${ADMIN_EMAIL}",
                mimeType: 'text/html'
            )
        }
    }
}