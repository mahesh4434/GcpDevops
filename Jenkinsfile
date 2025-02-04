pipeline {
    agent any
    environment {
        GOOGLE_PROJECT_ID = 'devopsgkestandardproject'
        GOOGLE_COMPUTE_ZONE = 'us-central1-a'
        PATH = "$PATH;C:\\terraform"
        LOG_FILE_PATH = 'D:\\New folder\\Logs\\pipeline_log.txt'
        HUGGINGFACE_API_URL = 'https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1'
        // Hardcoded Hugging Face API Token
    
    }
    stages {
        stage('Checkout SCM') {
            steps {
                script {
                    try {
                        checkout([$class: 'GitSCM', 
                            branches: [[name: '*/main']], 
                            userRemoteConfigs: [[url: 'https://github.com/mahesh4434/GcpDevops.git']]
                        ])
                        writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] Checkout SCM stage completed successfully.\n", append: true
                    } catch (Exception e) {
                        writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] Checkout SCM stage failed. Error: ${e.message}\n", append: true
                        error("Stopping pipeline due to error in Checkout SCM stage.")
                    }
                }
            }
        }

        stage('Pipeline Success Prediction') {
            steps {
                script {
                    try {
                        // 1. Terraform Syntax Validation
                        writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] Starting Terraform validation...\n", append: true
                        def tfValidation = bat(script: 'terraform validate', returnStatus: true)
                        if (tfValidation != 0) {
                            writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] Prediction: Terraform validation failed (Code: ${tfValidation})\n", append: true

                            // Simulate Popup with Input Step for user to continue or abort
                            def userResponse = input(
                                message: "Terraform validation failed. Please review the log below and choose whether to proceed or abort the pipeline:",
                                parameters: [
                                    text(name: 'Log Details', defaultValue: readFile(env.LOG_FILE_PATH), description: 'Full log of the error'),
                                    choice(name: 'Proceed with Pipeline?', choices: ['Proceed', 'Abort'], description: 'Do you want to continue with the pipeline?')
                                ]
                            )

                            if (userResponse == 'Abort') {
                                writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] Pipeline aborted by user.\n", append: true
                                error("Pipeline aborted by user after Terraform validation failure.")
                            }

                            writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] User chose to proceed with the pipeline despite Terraform validation failure.\n", append: true
                        }

                        // 2. File Structure Validation
                        writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] Validating file structure...\n", append: true
                        def requiredFiles = ['main.tf', 'variables.tf', 'outputs.tf']
                        requiredFiles.each { file -> 
                            if (!fileExists(file)) {
                                writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] Missing required file: ${file}\n", append: true
                                error("Missing critical Terraform file: ${file}")
                            }
                        }

                        // 3. Hugging Face API Analysis
                        writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] Starting AI analysis...\n", append: true
                        def pipelineCode = readFile('Jenkinsfile')
                        
                        // Using the hardcoded API token
                        def response = httpRequest(
                            acceptType: 'APPLICATION_JSON',
                            contentType: 'APPLICATION_JSON',
                            customHeaders: [[name: 'Authorization', value: "Bearer ${API_TOKEN}"]],
                            httpMode: 'POST',
                            requestBody: """
                            {
                                "inputs": "Analyze this Jenkins pipeline for potential issues. Consider the following aspects: 
                                1. Syntax errors
                                2. Security vulnerabilities
                                3. Configuration errors
                                4. Best practices
                                5. Resource conflicts
                                Pipeline code: ${pipelineCode}",
                                "parameters": {
                                    "max_length": 700,
                                    "temperature": 0.5,
                                    "top_p": 0.9
                                }
                            }""",
                            url: env.HUGGINGFACE_API_URL,
                            timeout: 30,
                            validResponseCodes: '200:499'
                        )

                        def logEntry = """
                        [${new Date()}] API Request Details:
                        - Status Code: ${response.status}
                        - Response: ${response.content}
                        """
                        writeFile file: env.LOG_FILE_PATH, text: logEntry + "\n", append: true

                        if (response.status == 200) {
                            def analysis = readJSON text: response.content
                            def generatedText = analysis[0].generated_text.toLowerCase()
                             
                            def warningKeywords = ['error', 'warning', 'issue', 'vulnerability', 'conflict', 'problem']
                            def foundIssues = warningKeywords.any { keyword -> generatedText.contains(keyword) }
                             
                            if (foundIssues) {
                                writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] AI Prediction: Potential issues detected\n", append: true
                                error("AI analysis detected potential issues - high failure probability")
                            }
                        } else {
                            writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] API request failed. Status: ${response.status}\n", append: true
                        }

                        writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] Prediction: All checks passed - high success probability\n", append: true

                    } catch (Exception e) {
                        writeFile file: env.LOG_FILE_PATH, text: "[${new Date()}] Prediction Failed: ${e.message}\n", append: true
                        error("Pipeline stopped due to prediction failure: ${e.message}")
                    }
                }
            }
        }

    }
    post {
        always {
            echo "Pipeline completed. Logs have been saved to ${env.LOG_FILE_PATH}"
            archiveArtifacts artifacts: env.LOG_FILE_PATH, allowEmptyArchive: true
        }
    }
}
