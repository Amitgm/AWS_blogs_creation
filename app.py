import boto3
import botocore.config 
import json
from datetime import datetime

def blog_generate_using_bedrock(blog_topic:str)-> str:

    prompt = f""" <s>[INST] Human: write 300 words on a topic  {blog_topic}

    Assistant: [/INST]
    """
    body = {"prompt":prompt,
            "max_gen_len":512,
            "temperature":0.5,
            "top_p":0.9
    }

    try:

        # create a client for Bedrock Runtime service with region name
        bedrock = boto3.client("bedrock-runtime",region_name="us-east-1",
                               config = botocore.config.Config(read_timeout=300,retries={"max_attempts":3}))
        
        # invoke the model with the prompt to generate the blog content response
        response = bedrock.invoke_model(body=json.dumps(body),modelId="meta.llama3-3-70b-instruct-v1:0")

        # read the whatever response obtained
        response_content = response.get("body").read()

        response_data = json.loads(response_content)

        print(response_data)

        blog_details = response_data["generation"]

        return blog_details

    except Exception as e:

        print("Failed to generate blog content.")

        return ""
    

def save_blog_details_s3(s3_key,s3_bucket,generate_blog):

    s3 = boto3.client("s3")

    try:

        s3.put_object(Key = s3_key, Bucket = s3_bucket, Body = generate_blog)

        print("code saved to s3")

    except:

        print("error when saving code to s3")


# the blog topic will be captured or triggers the event
def lambda_handler(event, context):

    event = json.loads(event["body"])

    blog_topic = event["blog"]

    genrate_blog = blog_generate_using_bedrock(blog_topic=blog_topic)

    if genrate_blog:

        current_time = datetime.now().strftime("%H:%M:%S")

        s3_key = f"blog-output/{current_time}.txt"

        s3_bucket = "aws_bucket_course1"

        save_blog_details_s3(s3_key, s3_bucket, genrate_blog)


    else:

        print("no blog was generated")

    return {
        'statusCode': 200,
        'body': json.dumps('Blog generated and saved to S3')
    }



