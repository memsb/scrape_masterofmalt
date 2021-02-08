resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = var.code_bucket
  acl    = "private"

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    project = "lambda"
  }
}