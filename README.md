# AWS Bedrock Langchain Python CDK Stack

## Overview
Optimize AWS Lambda functions with Boto3 by adding the latest packages and creating Lambda layers using `aws-cdk.aws-lambda-python-alpha`. Avoid common errors, like the numpy module issue, by following the guide. Use provided code and insights to enhance performance across various development environments.


This AWS Cloud Development Kit (CDK) stack, named `AwsBedrockLangchainPythonCdkStack`, is designed to deploy AWS Lambda functions along with the necessary AWS Identity and Access Management (IAM) roles and policies. The stack includes the following components:

1. **IAM Roles and Policies:**
   - A Lambda execution role (`LambdaRole`) is created with permissions to access S3 buckets and the Bedrock service. It is associated with the `AWSLambdaBasicExecutionRole` managed policy and a custom policy (`bedrock_policy`) allowing specific Bedrock actions.

2. **Lambda Layers:**
   - Two Lambda layers, `boto3_lambda_layer` and `langchain_lambda_layer`, are defined with specific configurations for architecture and runtime. These layers contain Python dependencies for the Lambda functions.

3. **Lambda Functions:**
   - The stack deploys two Lambda functions, `boto3_bedrock_example_lambda` and `langchain_bedrock_example_lambda`, each with its own code, runtime settings, and associated layers.

4. **CDK NAG Suppressions:**
   - CDK NAG (Not a Good Idea) suppressions are applied to address specific warnings related to IAM policies. These suppressions ensure that the Lambda execution policy and associated resources comply with the intended access patterns.

---

### Installing the Latest Boto3 Package

To ensure you have the latest version of the Boto3 package, follow these steps:

1. **Create a Lambda Layer:**

   Use the `aws-cdk.aws-lambda-python-alpha` package to define a Lambda layer containing the latest Boto3 package.

   ```python
   boto3_lambda_layer = _alambda.PythonLayerVersion(self, 
              'boto3-lambda-layer',
              entry = './aws_bedrock_langchain_python_cdk/lambda/layer/boto3_latest/',
              compatible_architectures=[_lambda.Architecture.ARM_64],
              compatible_runtimes=[_lambda.Runtime.PYTHON_3_11],
   )
   ```

2. **Attach the Layer to Your Lambda Function:**

   Once the layer is created, attach it to your Lambda function to ensure access to the latest Boto3 package and its bedrock API calls.

   ```python
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
   ```

### Langchain Package Integration

Similarly, optimize your Lambda functions by installing the Langchain package. Follow the same process of creating a Lambda layer as with Boto3, replacing "boto3" in the `requirements.txt` file with "langchain," and then attach it to your function to leverage Langchain's capabilities.

1. **Create a Lambda Layer:**

   ```python
   langchain_lambda_layer = _alambda.PythonLayerVersion(self, 
              'langchain-lambda-layer',
              entry = './aws_bedrock_langchain_python_cdk/lambda/layer/langchain_latest/',
              compatible_architectures=[_lambda.Architecture.ARM_64],
              compatible_runtimes=[_lambda.Runtime.PYTHON_3_11],
   )
   ```

2. **Attach the Layer to Your Lambda Function:**

   ```python
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
   ```

### Avoiding Common Pitfalls

When creating Lambda layers, be mindful of specifying the compatible architecture, either ARM_64 or X86_64. Failure to define this may result in container image errors, such as the numpy module error. This error can manifest as:

```json
{
  "errorMessage": "Unable to import module 'index': Error importing numpy: you should not try to import numpy from its source directory; please exit the numpy source tree, and relaunch your python interpreter from there.",
  "errorType": "Runtime.ImportModuleError",
  "requestId": "977004a7-f205-481a-8b53-7a4b5bf48d2b",
  "stackTrace": []
}
```

To prevent this issue, **explicitly mention** the compatible architectures during the layer creation process.


## Useful commands

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
