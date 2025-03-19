pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USER = 'arbish09'
    }
    
    triggers {
        githubPush()  // Add GitHub webhook trigger
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm  // This will check out the branch that triggered the build
            }
        }
        
        stage('Login to Docker Hub') {
            environment {
                DOCKER_HUB_PASSWORD = credentials('DOCKER_HUB_PASSWORD')
            }
            steps {
                sh 'echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USER --password-stdin'
            }
        }
        
        stage('Build Images') {
            parallel {
                stage('Backend') {
                    steps {
                        sh "docker build -t $DOCKER_HUB_USER/backend:latest -t $DOCKER_HUB_USER/backend:${GIT_BRANCH.replaceAll('/', '-')}-${BUILD_NUMBER} -f backend/Dockerfile backend"
                    }
                }
                stage('Frontend') {
                    steps {
                        sh "docker build -t $DOCKER_HUB_USER/frontend:latest -t $DOCKER_HUB_USER/frontend:${GIT_BRANCH.replaceAll('/', '-')}-${BUILD_NUMBER} -f frontend/Dockerfile frontend"
                    }
                }
            }
        }
        
        stage('Push Images') {
            steps {
                sh 'docker push $DOCKER_HUB_USER/backend:latest'
                sh "docker push $DOCKER_HUB_USER/backend:${GIT_BRANCH.replaceAll('/', '-')}-${BUILD_NUMBER}"
                sh 'docker push $DOCKER_HUB_USER/frontend:latest'
                sh "docker push $DOCKER_HUB_USER/frontend:${GIT_BRANCH.replaceAll('/', '-')}-${BUILD_NUMBER}"
            }
        }

        stage('Ansible Deployment') {
            steps {
                sh "ansible-playbook deploy.yml -e docker_hub_user=$DOCKER_HUB_USER -e git_branch=${GIT_BRANCH.replaceAll('/', '-')} -e build_number=${BUILD_NUMBER}"
            }
        }
    }
    
    post {
        always {
            sh 'docker logout || true'
            echo 'Pipeline completed'
        }
        success {
            echo "Build successful for branch ${GIT_BRANCH}"
        }
        failure {
            echo "Build failed for branch ${GIT_BRANCH}"
        }
    }
}
