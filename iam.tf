##################### IAM Service Roles ########################
data "template_file" "lambda" {
  template = "${file("assume_role_policy.json.tpl")}"
}

resource "aws_iam_role" "example_serverless_lambda_role" {
  name                  = "example-serverless-lambda-role"
  description           = "example serverless lambda role"
  assume_role_policy    = "${data.template_file.lambda.rendered}"
  force_detach_policies = "true"
}

################# Lambda Custom Policy Creation ####################
data "template_file" "lambda_iam_role_policy" {
  template = "${file("iam_role_policy.json.tpl")}"
}
resource "aws_iam_policy" "lambda" {
  name        = "example-serverless-lambda-policy"
  description = "example serverless lambda policy"
  policy      = "${data.template_file.lambda_iam_role_policy.rendered}"
}

################## Lambda Custom Policy Attachment ###################
resource "aws_iam_role_policy_attachment" "lambda" {
  role       = "${aws_iam_role.lambda.name}"
  policy_arn = "${aws_iam_policy.lambda.arn}"
}