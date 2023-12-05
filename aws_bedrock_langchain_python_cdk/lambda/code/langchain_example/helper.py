import boto3

'''
Parameters: 
    model_name - From list below or "list_foundation_models"
    prompt - Input to the model, string accepted, no default
    max_tokens - Configures the maximum number of tokens in the generated response
    temperature - 0-1, highest probability (least creative) to lowest probability (most creative)
    top_p - defines a cut off based on the sum of probabilities of the potential choices.
    top_k - Top K defines the cut off where the model no longer selects the words

Models currently supported:
    amazon.titan-tg1-large
    ai21.j2-grande-instruct
    ai21.j2-jumbo-instruct
    anthropic.claude-instant-v1
    anthropic.claude-v1
    anthropic.claude-v1-100k
    anthropic.claude-v2
    anthropic.claude-v2-100k

Notes:
    I needed to add a bedrock VPC endpoint to avoid timeouts.
    Some endpoints take 10-15 seconds to respond, set lambda timeout accordingly.
    Expects an environment variable called "secret_name".  This is a Secrets Manager
        secret that contains AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_DEFAULT_REGION
        If your setup calls bedrock locally, make sure your Lambda permissions include bedrock access
        and remove the cross-account settings in the bedrock client calls.
    Youll need a layer for requests and one for the private version of boto3 that includes bedrock.
        https://towardsdatascience.com/building-custom-layers-on-aws-lambda-35d17bd9abbb

Working On:
    Better error handling, logging, and status responses
    Cohere (when its available)
'''

bedrock_client = boto3.client('bedrock')
bedrock_runtime_client = boto3.client('bedrock-runtime')

def call_list_models():

    model_list = bedrock_client.list_foundation_models()
    response = []
    for model in model_list['modelSummaries']:
        print(model['modelId'])
        response.append(model['modelId'])
    
    return response

