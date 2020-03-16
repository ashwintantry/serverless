provider "aws" {
  region  = "ap-south-1"
  skip_credentials_validation = true
  skip_requesting_account_id =true
  version = "2.15.0"
}
