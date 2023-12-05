from langchain.prompts import PromptTemplate
from langchain.llms import Bedrock
from langchain.chains import LLMChain
from helper import *

def lambda_handler(event, context):
    case_study = "Machine Learning engineer"  ## Software Developer, Web developer, Husband hahaha

    claude = Bedrock(
        model_id="anthropic.claude-v1",
    )
    claude.model_kwargs = {'temperature': 0.3, 'max_tokens_to_sample': 4096}
    
    template = """
    Human: How to be a good {case_study}?  \n Assistant:
    """
    
    prompt_template = PromptTemplate(
        input_variables=["case_study"],
        template=template
    )
    
    llm_chain = LLMChain(
        llm=claude, verbose=True, prompt=prompt_template
    )
    
    results = llm_chain(case_study)
    print(results["text"])

    return {
        'statusCode': 200,
        'case_results': results["text"]
    }

if __name__ == "__main__":
    lambda_handler(None, None)