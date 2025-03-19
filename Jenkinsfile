pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USER = credentials('docker-hub-username')
        BUILD_NUMBER = "${env.BUILD_NUMBER}"
    }
    
    triggers {
        githubPush()
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        
        stage('Login to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'docker-hub-password', variable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_HUB_USER --password-stdin'
                }
            }
        }
        
        stage('Build Images') {
            parallel {
                stage('Backend') {
                    steps {
                        sh 'docker build -t $DOCKER_HUB_USER/backend:$BUILD_NUMBER -t $DOCKER_HUB_USER/backend:latest -f backend/Dockerfile backend'
                    }
                }
                
                stage('Frontend') {
                    steps {
                        sh 'docker build -t $DOCKER_HUB_USER/frontend:$BUILD_NUMBER -t $DOCKER_HUB_USER/frontend:latest -f frontend/Dockerfile frontend'
                    }
                }
            }
        }
        
        stage('Push Images') {
            parallel {
                stage('Push Backend') {
                    steps {
                        sh 'docker push $DOCKER_HUB_USER/backend:$BUILD_NUMBER'
                        sh 'docker push $DOCKER_HUB_USER/backend:latest'
                    }
                }
                
                stage('Push Frontend') {
                    steps {
                        sh 'docker push $DOCKER_HUB_USER/frontend:$BUILD_NUMBER'
                        sh 'docker push $DOCKER_HUB_USER/frontend:latest'
                    }
                }
            }
        }
        
        stage('Deploy with Ansible') {
            steps {
                ansiblePlaybook(
                    playbook: 'deploy.yml',
                    extraVars: [
                        docker_hub_user: env.DOCKER_HUB_USER,
                        build_number: env.BUILD_NUMBER
                    ],
                    colorized: true
                )
            }
        }
    }
    
    post {
        always {
            sh 'docker logout'
        }
        
        success {
            echo 'Pipeline completed successfully!'
        }
        
        failure {
            echo 'Pipeline failed!'
        }
    }
}