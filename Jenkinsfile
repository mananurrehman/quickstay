pipeline {
    agent any

    environment {
        SONAR_HOME     = tool "Sonar"
        ORACLE_VM_IP   = '140.245.25.178'
        ORACLE_VM_USER = 'ubuntu'
        APP_DIR        = '/home/ubuntu/quickstay'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo '📥 Cloning QuickStay repository...'
                git url: 'https://github.com/mananurrehman/quickstay.git', branch: 'main'
                echo '✅ Code cloned successfully!'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo '🔍 Running SonarQube code quality scan...'
                withSonarQubeEnv('Sonar') {
                    sh '''
                        ${SONAR_HOME}/bin/sonar-scanner \
                            -Dsonar.projectName=quickstay \
                            -Dsonar.projectKey=quickstay \
                            -Dsonar.sources=app/ \
                            -Dsonar.python.version=3.11 \
                            -Dsonar.exclusions=**/migrations/**,**/venv/**,**/__pycache__/**,**/node_modules/**,**/static/images/**
                    '''
                }
                echo '✅ SonarQube analysis complete!'
            }
        }

        // stage('SonarQube Quality Gate') {
        //     steps {
        //         echo '⏳ Waiting for SonarQube quality gate...'
        //         timeout(time: 5, unit: 'MINUTES') {
        //             waitForQualityGate abortPipeline: false
        //         }
        //         echo '✅ Quality gate check complete!'
        //     }
        // }

        stage('Trivy Security Scan') {
            steps {
                echo '🔒 Running Trivy filesystem security scan...'
                sh '''
                    trivy fs --severity CRITICAL,HIGH \
                        --exit-code 0 \
                        --format table \
                        --skip-dirs venv,node_modules,migrations,.git \
                        . > trivy-report.txt 2>&1 || true
                    cat trivy-report.txt
                '''
                echo '✅ Trivy scan complete!'
            }
        }

        stage('OWASP Dependency Check') {
            steps {
                echo '🛡️ Running OWASP dependency check...'
                dependencyCheck additionalArguments: '''
                    --scan .
                    --format HTML
                    --format JSON
                    --out ./owasp-report
                    --exclude **/venv/**
                    --exclude **/node_modules/**
                    --exclude **/migrations/**
                    --disableYarnAudit
                ''', odcInstallation: 'OWASP'
                echo '✅ OWASP check complete!'
            }
        }

        stage('Deploy to Staging') {
            steps {
                echo '🚀 Deploying to Oracle Cloud server...'
                sshagent(['oracle-vm-ssh-testuser']) {
                    // Copy deploy.sh to server
                    sh '''
                        scp -o StrictHostKeyChecking=no \
                            deploy.sh \
                            ${ORACLE_VM_USER}@${ORACLE_VM_IP}:/tmp/deploy.sh
                    '''

                    // Make executable and run
                    sh '''
                        ssh -o StrictHostKeyChecking=no \
                            ${ORACLE_VM_USER}@${ORACLE_VM_IP} \
                            "chmod +x /tmp/deploy.sh && /tmp/deploy.sh main"
                    '''
                }
                echo '✅ Deployment complete!'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '🔍 Verifying deployment...'
                sshagent(['oracle-vm-ssh-testuser']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no \
                            ${ORACLE_VM_USER}@${ORACLE_VM_IP} \
                            "cd ${APP_DIR} && docker-compose ps"
                    '''
                }
                echo '✅ Verification complete!'
            }
        }
    }

    post {
        success {
            echo '''
            ==========================================
            ✅ PIPELINE SUCCESS!
            🌐 App: http://140.245.25.178:5000
            ==========================================
            '''
        }
        failure {
            echo '''
            ==========================================
            ❌ PIPELINE FAILED!
            Check logs above for errors.
            ==========================================
            '''
        }
        always {
            echo '🧹 Cleaning workspace...'
            cleanWs()
        }
    }
}