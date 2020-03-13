output "s3_bucket_name" {
  value = "aws_s3_bucket.tan3_test_serverless_s3.bucket"
}
output "s3_bucket_endpoint_name" {
  value = "aws_s3_bucket.tan3_test_serverless_s3.website_endpoint"
}
output "api_http" {
  value = "https://${aws_api_gateway_rest_api.example_serverless_api.id}.execute-api.ap-south-1.amazonaws.com/${aws_api_gateway_deployment.example_serverless_deploy.stage_name}"
}
output "curl" {
  value = "curl -H 'Content-Type: application/json' -X POST -d '{\"name\": \"Daniel\"}' https://${aws_api_gateway_rest_api.example_serverless_api.id}.execute-api.ap-south-1.amazonaws.com/${aws_api_gateway_deployment.example_serverless_deploy.stage_name}"
}
output "pool_id" {
  value = aws_cognito_user_pool.example_serverless_cognito_pool.id
}
output "client_id" {
  value = aws_cognito_user_pool_client.example_serverless_cognito_client.id
}
