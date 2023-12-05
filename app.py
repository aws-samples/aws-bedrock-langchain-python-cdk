#!/usr/bin/env python3
import cdk_nag
from aws_cdk import Aspects
import aws_cdk as cdk
from aws_bedrock_langchain_python_cdk.aws_bedrock_langchain_python_cdk_stack import AwsBedrockLangchainPythonCdkStack

app = cdk.App()
aws_bedrock_langchain_stack = AwsBedrockLangchainPythonCdkStack(app, "AwsBedrockLangchainPythonCdkStack",)

Aspects.of(app).add(cdk_nag.AwsSolutionsChecks(reports=True, verbose=True))

app.synth()
