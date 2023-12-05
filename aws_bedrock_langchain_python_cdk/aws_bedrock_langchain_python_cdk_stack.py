from aws_cdk import (
    Stack,
    Duration,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as _alambda,
    aws_iam as iam,
    Stack,
    Duration
)
from constructs import Construct
from cdk_nag import NagSuppressions

class AwsBedrockLangchainPythonCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bedrock_policy = iam.PolicyStatement(
            effect= iam.Effect.ALLOW,
            actions= [
                "bedrock:*",   
            ],
            resources= ["*"]
        )

        lambda_role = iam.Role(
            self,
            "LambdaRole",
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            description="Role to access s3 buckets and Bedrock service by lambda",
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaBasicExecutionRole'),
                                ]
        )
        lambda_role.add_to_principal_policy(bedrock_policy)

        boto3_lambda_layer = _alambda.PythonLayerVersion(self, 
                                                    'boto3-lambda-layer',
                                                    entry = './aws_bedrock_langchain_python_cdk/lambda/layer/boto3_latest/',
                                                    compatible_architectures=[_lambda.Architecture.ARM_64],
                                                    compatible_runtimes=[_lambda.Runtime.PYTHON_3_11],
        )

        langchain_lambda_layer = _alambda.PythonLayerVersion(self, 
                                                    'langchain-lambda-layer',
                                                    entry = './aws_bedrock_langchain_python_cdk/lambda/layer/langchain_latest/',
                                                    compatible_architectures=[_lambda.Architecture.ARM_64],
                                                    compatible_runtimes=[_lambda.Runtime.PYTHON_3_11 ],
        )

        boto3_bedrock_example_lambda = _lambda.Function(
            self,
            "boto3_bedrock_example_lambda",
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("./aws_bedrock_langchain_python_cdk/lambda/code/boto3_example/"),
            runtime=_lambda.Runtime.PYTHON_3_11,
            architecture=_lambda.Architecture.ARM_64,
            role=lambda_role,
            layers=[
                boto3_lambda_layer
            ],
            timeout=Duration.seconds(300),
            memory_size=1024,
        )

        langchain_bedrock_example_lambda = _lambda.Function(
            self,
            "langchain-bedrock-example-lambda",
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("./aws_bedrock_langchain_python_cdk/lambda/code/langchain_example/"),
            runtime=_lambda.Runtime.PYTHON_3_11,
            architecture=_lambda.Architecture.ARM_64,
            role=lambda_role,
            layers=[
                boto3_lambda_layer,
                langchain_lambda_layer
            ],
            timeout=Duration.seconds(300),
            memory_size=1024,
        )

        # CDK NAG suppression
        NagSuppressions.add_stack_suppressions(self, [
                                            {
                                                "id": 'AwsSolutions-IAM4',
                                                "reason": 'Lambda execution policy for custom resources created by higher level CDK constructs',
                                                "appliesTo": [
                                                        'Policy::arn:<AWS::Partition>:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
                                                    ],
                                            }])
        
        NagSuppressions.add_resource_suppressions(lambda_role,
                            suppressions=[{
                                            "id": "AwsSolutions-IAM5",
                                            "reason": "Lambda needs * access to all objects inside S3 bucket. And Bedrock all actions are allowed",
                                            }
                                        ],
                            apply_to_children=True)