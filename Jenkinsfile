pipeline {
  agent any
  stages {
    stage('Clone Repository') {
      steps {
        git branch: 'main', url: 'https://github.com/bishal4965/CI-CD-pipeline-jenkins.git'
      }
    }
    stage('Build Backend Image') {
      steps {
        sh 'docker build -t localhost:5000/backend:latest -f backend/Dockerfile backend'
      }
    }
    stage('Build Frontend Image') {
      steps {
        sh 'docker build -t localhost:5000/frontend:latest -f frontend/Dockerfile frontend'
      }
    }
    stage('Push Images to Local Registry') {
      steps {
        sh 'docker push localhost:5000/backend:latest'
        sh 'docker push localhost:5000/frontend:latest'
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        sh 'kubectl apply -f k8s/'
      }
    }
  }
  post {
    always {
      echo 'Pipeline completed'
    }
  }
}