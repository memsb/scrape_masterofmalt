resource "aws_iam_role" "build_lambda_role" {
  name = "build_lambda_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudformation.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

  tags = {
    project = var.project
  }
}

resource "aws_iam_role_policy" "build_lambda_policy" {
  role = aws_iam_role.build_lambda_role.name

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "arn:aws:logs:*:*:log-group:${var.app}-group:*"
      ],
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "${aws_s3_bucket.codepipeline_bucket.arn}",
        "${aws_s3_bucket.codepipeline_bucket.arn}/*"
      ]
    },
    {
      "Sid": "codebuild",
      "Effect": "Allow",
      "Action": [
        "codebuild:UpdateReport",
        "codebuild:CreateReport",
        "codebuild:CreateReportGroup",
        "codebuild:BatchPutCodeCoverages",
        "codebuild:BatchPutTestCases",
        "codedeploy:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "cloudformation",
      "Effect": "Allow",
      "Action": [
        "cloudformation:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "events",
      "Effect": "Allow",
      "Action": [
        "events:PutRule",
        "events:ListRules",
        "events:RemoveTargets",
        "events:ListTargetsByRule",
        "events:TagResource",
        "events:PutTargets",
        "events:DeleteRule",
        "events:UntagResource",
        "events:DescribeRule"
      ],
      "Resource": "*"
    },
    {
      "Sid": "iam",
      "Effect": "Allow",
      "Action": [
        "iam:UntagRole",
        "iam:TagRole",
        "iam:CreateRole",
        "iam:AttachRolePolicy",
        "iam:PutRolePolicy",
        "iam:PassRole",
        "iam:DeleteRolePolicy",
        "iam:DetachRolePolicy",
        "iam:GetRole",
        "iam:DeleteRole",
        "iam:UntagUser",
        "iam:TagUser",
        "iam:GetRolePolicy"
      ],
      "Resource": "*"
    },
    {
      "Sid": "lambda",
      "Effect": "Allow",
      "Action": [
        "lambda:*"
      ],
      "Resource": "arn:aws:lambda:*:*:function:${var.app}"
    }
  ]
}
POLICY
}