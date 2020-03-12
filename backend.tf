terraform {
  backend "s3" {
    bucket         = "example-serverless-tan3-terraform-state-s3"
    key            = "serverless/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
  }
}