resource "aws_codebuild_project" "codebuild" {
  name = var.app
  description = "build ${var.app}"
  build_timeout = "5"
  service_role = aws_iam_role.build_lambda_role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  cache {
    type = "S3"
    location = aws_s3_bucket.codepipeline_bucket.bucket
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image = "aws/codebuild/amazonlinux2-x86_64-standard:3.0"
    type = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"

    environment_variable {
      name  = "BUCKET"
      value = aws_s3_bucket.codepipeline_bucket.bucket
    }
  }

  logs_config {

    cloudwatch_logs {
      group_name = "${var.app}-group"
      stream_name = "${var.app}-stream"
    }

    s3_logs {
      status = "ENABLED"
      location = "${aws_s3_bucket.codepipeline_bucket.id}/build-log"
    }
  }

  source {
    type = "CODEPIPELINE"
  }

  source_version = "main"

  tags = {
    project = var.project
  }
}
