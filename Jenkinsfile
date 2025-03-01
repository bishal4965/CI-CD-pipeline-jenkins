pipeline {
  agent any
  environment {
    DOCKER_HUB_USER = 'arbish09'
  }
  stages {
    stage('Clone Repository') {
      steps {
        git branch: 'main', url: 'https://github.com/bishal4965/CI-CD-pipeline-jenkins.git'
      }
    }
    stage('Login to Docker Hub') {
      environment {
        DOCKER_HUB_PASSWORD = credentials ('DOCKER_HUB_PASSWORD')  // Use stored credentials
      }
      steps {
        sh 'echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USER --password-stdin'
      }
    }
    stage('Set Kubernetes Context') {
      steps {
        // Set the correct kubectl context
        sh 'kubectl config use-context minikube'
      }
    }
    stage('Build Backend Image') {
      steps {
        sh 'docker build -t $DOCKER_HUB_USER/backend:latest -f backend/Dockerfile backend'
      }
    }
    stage('Build Frontend Image') {
      steps {
        sh 'docker build -t $DOCKER_HUB_USER/frontend:latest -f frontend/Dockerfile frontend'
      }
    }
    stage('Push Images to Docker Hub') {
      steps {
        sh 'docker push $DOCKER_HUB_USER/backend:latest'
        sh 'docker push $DOCKER_HUB_USER/frontend:latest'
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        sh 'kubectl apply -f k8s/03-backend.yaml'
        sh 'kubectl apply -f k8s/04-frontend.yaml'
      }
    }
  }
  post {
    always {
      echo 'Pipeline completed'
    }
  }
}
