bitbucket-codebuild-trigger
===========================

This is a Bitbucket-compatible webhook that triggers an existing
CodeBuild project. It is built using the Serverless Application Model
and uses Lambda and API Gateway.

Usage
-----

1. Deploy the code with `deploy.sh`. The script will output the endpoint URL:
   ```Endpoint: https://xyzabc1234.execute-api.us-east-1.amazonaws.com/Prod/trigger```
   
2. In your Bitbucket repository settings, open the Webhooks section
   and click "Add webhook".
   
3. Provide the Title as "CodeBuild" and the URL as the endpoint
   retrieved from step 1, with `?projectName=my-codebuild-project`
   appended. Set the trigger to "Repository push".
   
4. Push a test commit to your repo. In Bitbucket, you should see the
   webhook be called; in AWS CloudWatch Logs, you should see a log
   entry for the function call.
   
