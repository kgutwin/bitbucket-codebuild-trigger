import json
import boto3

codebuild = boto3.client('codebuild')

def respond(body, err=None):
    if not body:
        return {'statusCode': '204', 'body': ''}
    
    return {
        'statusCode': '400' if err else '200',
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }


def lambda_handler(event, context):
    print("Received event:")
    print(json.dumps(event))
    #print(event['headers'])
    if not event['headers'].get('X-Event-Key') == 'repo:push':
        return respond({'message': 'not a repo:push'}, err=True)

    if (event['queryStringParameters'] is None
        or 'projectName' not in event['queryStringParameters']):
        return respond({'message': 'projectName query parameter not specified'},
                       err=True)
    project_name = event['queryStringParameters']['projectName']
    
    body = json.loads(event['body'])

    builds = []
    for change in body['push']['changes']:
        new_target = change['new']['target']['hash']
        idempotency_token = event['headers'].get(
            'X-Request-UUID',
            event['requestContext']['requestId'])

        print(f"triggering codebuild.start_build(projectName='{project_name}', sourceVersion='{new_target}', idempotencyToken='{idempotency_token}')")
        response = codebuild.start_build(
            projectName=project_name,
            sourceVersion=new_target,
            idempotencyToken=idempotency_token)
        
        builds.append(response['build']['arn'])
    
    return respond({'message': 'success', 'builds': builds})
