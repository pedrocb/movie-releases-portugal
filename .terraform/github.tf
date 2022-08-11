data "aws_caller_identity" "current" {}

resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = [
    "sts.amazonaws.com"
  ]
  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1"
  ]
}

resource "aws_iam_role" "github_actions" {
  name = "movie-releases-github-actions"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Principal": {
                "Federated": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
            },
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": "repo:pedrocb/movie-releases-portugal:*"
                }
            }
        }
    ]
}
EOF
}

resource "aws_iam_policy" "build_push_ecr" {
  name = "BuildPublishECR"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
	Effect =  "Allow",
	Action = [
	  "ecr:CompleteLayerUpload",
	  "ecr:UploadLayerPart",
	  "ecr:InitiateLayerUpload",
	  "ecr:BatchCheckLayerAvailability",
	  "ecr:PutImage"
	],
	Resource = "${aws_ecr_repository.movie_releases_pt.arn}"
      },
      {
	Effect = "Allow",
	Action = "ecr:GetAuthorizationToken",
	Resource = "*"
      }
    ]
  })

}

resource "aws_iam_policy" "update_lambda_function" {
  name = "UpdateLambdaFunction"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
	Effect =  "Allow",
	Action = [
	  "lambda:UpdateFunctionCode",
	],
	Resource = "${aws_lambda_function.movie_releases_pt.arn}"
      },
    ]
  })

}

resource "aws_iam_role_policy_attachment" "github_actions_build_publish_ecr" {
  role = aws_iam_role.github_actions.name
  policy_arn = aws_iam_policy.build_push_ecr.arn
}

resource "aws_iam_role_policy_attachment" "github_actions_update_lambda_function" {
  role = aws_iam_role.github_actions.name
  policy_arn = aws_iam_policy.update_lambda_function.arn
}
