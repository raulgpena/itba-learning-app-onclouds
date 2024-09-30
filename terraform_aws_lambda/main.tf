
resource "aws_iam_role" "lambda_exec" {
    
    name = "lambda_exec_role"

    assume_role_policy = jsonencode({
      Version = "2012-10-17",
      
      Statement = [
        {
          Action = "sts:AssumeRole",
          Effect = "Allow",
          Sid    = "",
          Principal = {
            Service = "lambda.amazonaws.com"
          }
        }
      ]
    })
}


resource "aws_iam_role_policy_attachment" "lambda_exec_policy" {

    depends_on = [aws_iam_role.lambda_exec]
    
    role       = aws_iam_role.lambda_exec.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


resource "aws_lambda_function" "api_lambda" {
    
    depends_on = [aws_lambda_function.api_lambda]

    filename         = "lambda_function.zip"
    function_name    = "flask_api_lambda"
    role             = aws_iam_role.lambda_exec.arn
    handler          = "lambda_function.lambda_handler"
    runtime          = "python3.8"
    source_code_hash = filebase64sha256("lambda_function.zip")
    memory_size      = 1024
    timeout          = 30
}


resource "aws_api_gateway_rest_api" "api" {
    
    depends_on = [aws_lambda_function.api_lambda]

    name        = "flask_api"
    description = "API Gateway for Flask Lambda"
}


resource "aws_api_gateway_resource" "resource" {
  
    depends_on = [aws_api_gateway_rest_api.api]

    rest_api_id = aws_api_gateway_rest_api.api.id
    parent_id   = aws_api_gateway_rest_api.api.root_resource_id
    path_part   = "{proxy+}"
}


resource "aws_api_gateway_method" "method" {

    depends_on = [aws_api_gateway_rest_api.api,
                  aws_api_gateway_resource.resource]
    
    rest_api_id   = aws_api_gateway_rest_api.api.id
    resource_id   = aws_api_gateway_resource.resource.id
    http_method   = "ANY"
    authorization = "NONE"
}


resource "aws_api_gateway_method" "root_method" {
    rest_api_id   = aws_api_gateway_rest_api.api.id
    resource_id   = aws_api_gateway_rest_api.api.root_resource_id
    http_method   = "ANY"
    authorization = "NONE"
}


resource "aws_api_gateway_integration" "root_integration" {
    rest_api_id             = aws_api_gateway_rest_api.api.id
    resource_id             = aws_api_gateway_rest_api.api.root_resource_id
    http_method             = aws_api_gateway_method.root_method.http_method
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.api_lambda.invoke_arn
}


resource "aws_api_gateway_integration" "integration" {
    
    depends_on = [aws_api_gateway_rest_api.api,
                  aws_api_gateway_resource.resource,
                  aws_api_gateway_method.method]

    rest_api_id             = aws_api_gateway_rest_api.api.id
    resource_id             = aws_api_gateway_resource.resource.id
    http_method             = aws_api_gateway_method.method.http_method
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.api_lambda.invoke_arn
}


resource "aws_lambda_permission" "api_gateway" {
    
    depends_on = [aws_lambda_function.api_lambda]

    statement_id  = "AllowAPIGatewayInvoke"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.api_lambda.function_name
    principal     = "apigateway.amazonaws.com"
    source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}


resource "aws_api_gateway_deployment" "api_deployment" {
    
    depends_on = [aws_api_gateway_integration.integration]

    rest_api_id = aws_api_gateway_rest_api.api.id
    stage_name = "prod"

    triggers = {
        redeployment = "${timestamp()}"
    }
}


output "api_url" {
    
    value = "https://${aws_api_gateway_rest_api.api.id}.execute-api.us-east-1.amazonaws.com/prod/"
}