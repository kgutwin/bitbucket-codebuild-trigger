#!/bin/bash

set -e

STACK_NAME=bitbucket-codebuild-trigger
S3_BUCKET=$(aws s3 ls | awk '/sam-deployments/{print $NF}')
if [[ -z $S3_BUCKET ]]; then
    S3_BUCKET=sam-deployments-$RANDOM$RANDOM
    aws s3 mb s3://$S3_BUCKET
fi

sam package --template-file template.yaml \
    --output-template-file serverless-output.yaml \
    --s3-bucket $S3_BUCKET

sam deploy --template-file serverless-output.yaml \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_IAM

APIID=$(aws apigateway get-rest-apis \
            --query 'items[?name==`'$STACK_NAME'`].[id]' \
            --output text)
REGION=${AWS_DEFAULT_REGION:-$(aws configure get region)}

echo "Endpoint: https://${APIID}.execute-api.${REGION}.amazonaws.com/Prod/trigger"
