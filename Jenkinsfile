pipeline{
    agent any
    parameters{
        
        choice(name:'ENVTYPE',choices:['Nginx','NodeJS'],description:'Type of Environment to launch like Nginx, tomcat etc. This will be used for bootstrapping')
        string(name:'BUCKETNAME',description:'S3 Bucket for keys')
        string(name:'EC2KEY',description:'Key name for EC2 login')
        string(name:'AWS_DEFAULT_REGION')

    }
    environment{
        env="production"
    }
    stages{
        stage('Deploy Infra and Launch Instance'){
            when{
                environment name: 'env', value: 'production'
            }
            steps{
                withAWS(credentials: 'awscreds', region: ${env.AWS_DEFAULT_REGION}) {
                script {

                    env.STACKID = sh(label:'',script:"aws cloudformation create-stack --stack-name demoec2instance --template-body file://deploy_ec2_network.json --parameters ParameterKey=KeyP,ParameterValue=${env.EC2KEY} ParameterKey=InstanceType,ParameterValue=t2.micro --query StackId",returnStdout: true).trim()
                    env.STACKSTATUS=sh(label:'',script:"aws cloudformation describe-stacks --stack-name ${env.STACKID} --query Stacks[0].StackStatus",returnStdout: true).trim()
                        while("${env.STACKSTATUS}"=='"CREATE_IN_PROGRESS"'){
                            sleep(20)
                            env.STACKSTATUS=sh(label:'',script:"aws cloudformation describe-stacks --stack-name ${env.STACKID} --query Stacks[0].StackStatus",returnStdout: true).trim()
                        }
                        env.INSTIP=sh(label:'',script:"aws cloudformation describe-stacks --stack-name ${env.STACKID} --query Stacks[0].Outputs[2].OutputValue",returnStdout: true).trim()
                    }
                }
            }
       // stage('Bootstrap'){
       //     steps{

       //     }
        stage('Record Instance IP/DNS'){
            steps{
                sh "echo ${env.INSTIP}>InstanceDNS.txt"
                archiveArtifacts 'InstanceDNS.txt'
            }
        }
    }
    post{
        success{
            cleanWs disableDeferredWipeout: true, deleteDirs: true
        }
        failure{
            sh "aws cloudformation delete-stack --stack-name ${env.STACKID}"
            cleanWs disableDeferredWipeout: true, deleteDirs: true
        }
    }
    }   
}