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
        DOCKER_HUB_PASSWORD = credentials('DOCKER_HUB_PASSWORD')  // Use stored credentials
      }
      steps {
        sh 'echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USER --password-stdin'
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
    stage('Run Backend Container') {
      steps {
        sh 'docker run -d --name backend -p 8080:8080 $DOCKER_HUB_USER/backend:latest'
      }
    }
    stage('Run Frontend Container') {
      steps {
        sh 'docker run -d --name frontend -p 80:80 $DOCKER_HUB_USER/frontend:latest'
      }
    }
  }
  post {
    always {
      echo 'Pipeline completed'
    }
  }
}
