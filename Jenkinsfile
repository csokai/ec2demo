pipeline{
    agent any
    parameters{
        
        string(name:'BUCKETNAME',description:'S3 Bucket for keys')
        string(name:'EC2KEY',description:'Key name for EC2 login')
        string(name:'AWS_DEFAULT_REGION')

    }
    environment{
        env="demo"
        STACKID=""
        STACKSTATUS=""
        INSTIP=""
    }
    stages{
        stage('Deploy Infra and Launch Instance'){
            when{
                environment name: 'env', value: 'demo'
            }
            steps{
                withAWS(credentials: 'awscreds', region: "${AWS_DEFAULT_REGION}") {
                script {

                    STACKID = sh(label:'',script:"aws cloudformation create-stack --stack-name demoec2instance --template-body file://deploy_ec2_network.json --parameters ParameterKey=KeyP,ParameterValue=${EC2KEY} ParameterKey=InstanceType,ParameterValue=t2.micro --query StackId",returnStdout: true).trim()
                    STACKSTATUS=sh(label:'',script:"aws cloudformation describe-stacks --stack-name ${STACKID} --query Stacks[0].StackStatus",returnStdout: true).trim()
                        while("${STACKSTATUS}"=='"CREATE_IN_PROGRESS"'){
                            sleep(20)
                            STACKSTATUS=sh(label:'',script:"aws cloudformation describe-stacks --stack-name ${STACKID} --query Stacks[0].StackStatus",returnStdout: true).trim()
                        }
                        INSTIP=sh(label:'',script:"aws cloudformation describe-stacks --stack-name ${STACKID} --query Stacks[0].Outputs[2].OutputValue",returnStdout: true).trim()
                    }
                }
            }
        }
        stage('Record Instance IP/DNS'){
            steps{
                sh "echo ${INSTIP}>InstanceDNS.txt"
                archiveArtifacts 'InstanceDNS.txt'
            }
        }
    }
    post{
        success{
            cleanWs disableDeferredWipeout: true, deleteDirs: true
        }
        failure{
            sh "aws cloudformation delete-stack --stack-name ${STACKID}"
            cleanWs disableDeferredWipeout: true, deleteDirs: true
        }
    }   
}