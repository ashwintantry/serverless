terraform {
  backend "local" {
    path = "/var/lib/jenkins/workspace/sl-test/terraform.tfstate"
  }
}
