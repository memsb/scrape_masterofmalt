resource "aws_codepipeline" "codepipeline" {
  name     = var.app
  role_arn = aws_iam_role.codepipeline_role.arn

  artifact_store {
    location = aws_s3_bucket.codepipeline_bucket.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "ThirdParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = [var.app]

      configuration = {
        Owner                = var.github_org
        Repo                 = var.project
        PollForSourceChanges = "true"
        Branch               = "main"
        OAuthToken           = var.github_token
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = [var.app]
      output_artifacts = ["build_output"]
      version          = "1"

      configuration = {
        ProjectName = var.app
      }
    }
  }

  stage {
    name = "Prepare"

    action {
      name            = "build_templates"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "CloudFormation"
      input_artifacts = ["build_output"]
      version         = "1"

      configuration = {
        ActionMode     = "CHANGE_SET_REPLACE"
        Capabilities   = "CAPABILITY_NAMED_IAM,CAPABILITY_IAM"
        OutputFileName = "CreateStackOutput.json"
        ChangeSetName  = "${var.stack}Set"
        StackName      = var.stack
        TemplatePath   = "build_output::outputtemplate.yml"
        RoleArn        = aws_iam_role.build_lambda_role.arn
      }
    }
  }

  stage {
    name = "Deploy"

    action {
      name            = "execute_templates"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "CloudFormation"
      input_artifacts = ["build_output"]
      version         = "1"

      configuration = {
        ActionMode     = "CHANGE_SET_EXECUTE"
        Capabilities   = "CAPABILITY_NAMED_IAM,CAPABILITY_IAM"
        OutputFileName = "CreateStackOutput.json"
        ChangeSetName  = "${var.stack}Set"
        StackName      = var.stack
        TemplatePath   = "build_output::outputtemplate.yml"
        RoleArn        = aws_iam_role.build_lambda_role.arn
      }
    }
  }

  tags = {
    Project = var.project
  }
}