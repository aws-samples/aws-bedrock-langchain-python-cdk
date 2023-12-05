from helper import *

def lambda_handler(event, context):
    prompt = "How to be a good Machine Learning engineer?"

    model_list= call_list_models()
    print(model_list)
    results_claude = call_bedrock_anthropic(prompt, model_name = "anthropic.claude-v1")
    print(results_claude)
    results_anthropic = call_bedrock_jurassic(prompt, )
    print(results_anthropic)
    results_titan = call_bedrock_titan(prompt,)
    print(results_titan)

    return {
        'statusCode': 200,
        'model_list': str(model_list),
        'results_claude': results_claude,
        'results_anthropic': results_anthropic,
        'results_titan': results_titan
    }

if __name__ == "__main__":
    lambda_handler(None, None)