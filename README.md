# the following must be done for AWS to invoke a model for Blog Generation

NOTE: BEFORE STRATING ANYTHING MAKE SURE YOU SELCECT THE REGION FOR ALL YOUR FEATURES IN THIS CASE us-east-1

A Lambda function must be created (select your python version, architecture microsoft one and what python versions to be compatible with) and the code written must be placed in the code cell.

Add the layer to the Lambda function with following steps:

pip install boto3 -t python for using the latest boto3

Zip file the libraries underneath the python directory

Create a layer to append to the Lambda function with the zip file.


Model from the AWS bedrock must be granted access before starting

go to IAM (Identity Access Management) to give access permissions to all the features you are using.

To do that select the configuration of the Lambda function and click the role name. From there go to add permissions
and select attach policie and select AdministratorAccess this give access to invoke your models

Next step is to test your Lambda function code and see if everything is working properly.

Make sure the code you write for test, is different from the code you write for the API call using API gateway.

Once this works, create the API gateway, by going to the API gateway and doing the following steps:

    Create a HTTP API, give it a name, review and create. 

    create a route for it by selecting the Post method and giving it a name, 
    
    Next attach an integration with integration Type set as Lambda and selcting the appropriate Lamda function

    Then create a stage (for a certain environment, create a stage name called dev, you have the url to deploy) then selcet the deploy button, the url is the path given in your dev environment for example: https://ukauet6749.execute-api.us-east-1.amazonaws.com/dev with blog-generate in your Routes /blog-generate together the url id:

    https://ukauet6749.execute-api.us-east-1.amazonaws.com/dev/blog-generate

    Then after that create the s3 bucket, make sure when creating the bucket, the same name is given in your code.


    make the post request in your postman with the example :

    {

        "blog": "what is machine learning"
    }


After this got to logs in the Cloudwatch under log groups, select the link with /aws/lamda/{your lamda function} and see the recent logs under the log streams