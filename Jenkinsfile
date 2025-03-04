pipeline {
    agent any
    
    environment {
        DOCKER_HUB_TOKEN = credentials('docker-hub-token')
        APP_NAME = 'mlops-a01'
        DOCKER_IMAGE = "ahmed93560/${APP_NAME}:${env.BUILD_NUMBER}"
        DOCKER_USERNAME = 'ahmed93560'
        ADMIN_EMAIL = 'ahmedkhanraza935@gmail.com'
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
        
        stage('Push to Docker Hub') {
            steps {
                bat "echo %DOCKER_HUB_TOKEN% | docker login -u %DOCKER_USERNAME% --password-stdin"
                bat "docker push ${DOCKER_IMAGE}"
                bat "docker tag ${DOCKER_IMAGE} %DOCKER_USERNAME%/${APP_NAME}:latest"
                bat "docker push %DOCKER_USERNAME%/${APP_NAME}:latest"
                bat "docker logout"
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