pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = 'arbish09'
    }
    stages {
        // ANSIBLE HANDLES THE CLEANUP PROCESS //
        /*
        stage('Clean Previous Containers') {
            steps {
                sh 'docker stop frontend backend || true'
                sh 'docker rm frontend backend || true'
            }
        }
        */
        // ANSIBLE HANDLES THE CLEANUP PROCESS //

        stage('Clone Repository') {
            steps {
                git branch: '*/${GIT_BRANCH}', url: 'https://github.com/bishal4965/CI-CD-pipeline-jenkins.git'
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
                        sh 'docker build -t $DOCKER_HUB_USER/backend:latest -f backend/Dockerfile backend'
                    }
                }
                stage('Frontend') {
                    steps {
                        sh 'docker build -t $DOCKER_HUB_USER/frontend:latest -f frontend/Dockerfile frontend'
                    }
                }
            }
        }
        stage('Push Images') {
            steps {
                sh 'docker push $DOCKER_HUB_USER/backend:latest'
                sh 'docker push $DOCKER_HUB_USER/frontend:latest'
            }
        }

        // ANSIBLE HANDLES THE DEPLOYMENT //
        /*
        stage('Deploy Containers') {
            steps {
                sh 'docker network create mynetwork || true'
                sh 'docker run -d --name backend --network mynetwork -v $(pwd)/backend:/app -p 5000:5000 $DOCKER_HUB_USER/backend:latest'
                sh 'sleep 5'  // Wait for backend to initialize
                sh 'docker run -d --name frontend --network mynetwork -p 80:80 $DOCKER_HUB_USER/frontend:latest'
            }
        }
        */
        // ANSIBLE HANDLES THE DEPLOYMENT //

        stage('Ansible Deployment') {
            steps {
                sh 'ansible-playbook deploy.yml -e docker_hub_user=$DOCKER_HUB_USER'
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed'
        }
    }
}
