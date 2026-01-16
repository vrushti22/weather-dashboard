pipeline {
    agent any

    environment {
        IMAGE_NAME = "weather-app"
        CONTAINER_NAME = "weather"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Container') {
            steps {
                sh "docker rm -f ${CONTAINER_NAME} || true"
                sh "docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}"
            }
        }
    }

    post {
        success {
            echo "Weather app deployed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
