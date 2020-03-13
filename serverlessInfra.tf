resource "aws_s3_bucket" "tan3_test_serverless_s3" {
  bucket = "tan3-test-serverless"
  acl    = "public-read"
  website {
    index_document = "index.html"
    }

  tags = merge(
    map("Classification", "public"),
    map("Name", "serverlessTest")
  )
}

resource "aws_cognito_user_pool" "example_serverless_cognito_pool" {
  name = "example-serverless-cognito-pool"
}

resource "aws_cognito_user_pool_client" "example_serverless_cognito_client" {
  name = "example-serverless-cognito-client"
  
  user_pool_id = "${aws_cognito_user_pool.example_serverless_cognito_pool.id}"
  generate_secret     = false
}

resource "aws_lambda_function" "lambda_serverless" {
  function_name    = "example-serverless-lambda"
  filename         = "requestUnicorn.zip"
  description      = "example serverless lambda"
  role             = "${aws_iam_role.example_serverless_lambda_role.arn}"
  handler          = "requestUnicorn.handler"
  memory_size      = 512
  source_code_hash = "${filebase64sha256("requestUnicorn.zip")}"
  runtime          = "nodejs10.x"
  timeout          = 60
  tags = merge(
    map("Name", "serverlessTest")
  )
}

resource "aws_api_gateway_rest_api" "example_serverless_api" {
  name        = "example-serverless-api"
  description = "example serverless api"
  endpoint_configuration {
    types = ["EDGE"]
  }
}

resource "aws_api_gateway_resource" "example_serverless_api_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.example_serverless_api.id}"
  parent_id   = "${aws_api_gateway_rest_api.example_serverless_api.root_resource_id}"
  path_part   = "ride"
}

data "aws_cognito_user_pools" "selected" {
  name = "example-serverless-cognito-pool"
}

resource "aws_api_gateway_authorizer" "example_serverless_cognito" {
  name          = "cognito"
  type          = "COGNITO_USER_POOLS"
  rest_api_id   = "${aws_api_gateway_rest_api.example_serverless_api.id}"
  provider_arns = ["${aws_cognito_user_pools.selected.arns}"]
}

resource "aws_api_gateway_method" "example_serverless_api_method" {
  rest_api_id   = "${aws_api_gateway_rest_api.example_serverless_api.id}"
  resource_id   = "${aws_api_gateway_resource.example_serverless_api_resource.id}"
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = "${aws_api_gateway_authorizer.example_serverless_cognito.id}"
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = "${aws_api_gateway_rest_api.example_serverless_api.id}"
  resource_id             = "${aws_api_gateway_resource.example_serverless_api_resource.id}"
  http_method             = "${aws_api_gateway_method.example_serverless_api_method.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.lambda_serverless.invoke_arn}"
}

resource "aws_api_gateway_deployment" "example_serverless_deploy" {
  depends_on = ["aws_api_gateway_integration.integration"]
  stage_name  = "prod"
  rest_api_id = "${aws_api_gateway_rest_api.example_serverless_api.id}"
}
