resource "aws_ecr_repository" "movie_releases_pt" {
  name = "movie-releases-portugal"
  force_delete = true
}

resource "aws_ecr_lifecycle_policy" "cleanup" {
  repository = aws_ecr_repository.movie_releases_pt.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Keep last 1 images",
            "selection": {
                "tagStatus": "any",
                "countType": "imageCountMoreThan",
                "countNumber": 1
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}

resource "aws_iam_role" "movie_releases_pt_lambda" {
  name = "movie-releases-iam-lambda"
  assume_role_policy = <<EOF
{
"Version": "2012-10-17",
"Statement": [{
    "Action": "sts:AssumeRole",
    "Principal": {
      "Service": "lambda.amazonaws.com"
    },
    "Effect": "Allow",
    "Sid": ""
  }]
}
EOF
}

resource "aws_iam_role_policy_attachment" "cloudwatch_logs" {
  role = aws_iam_role.movie_releases_pt_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "movie_releases_pt" {
  function_name = "UpdateMovieReleasesDaily"
  role = aws_iam_role.movie_releases_pt_lambda.arn
  image_uri = "${aws_ecr_repository.movie_releases_pt.repository_url}:latest"
  package_type = "Image"
  timeout = 600
}

resource "aws_cloudwatch_event_rule" "once_a_day" {
  name = "once-a-day"
  description = "Daily event trigger"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "moviereleases_daily" {
  rule = "${aws_cloudwatch_event_rule.once_a_day.name}"
  target_id = "lambda"
  arn = "${aws_lambda_function.movie_releases_pt.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_moviereleases" {
  statement_id = "AllowExecutionFromCloudwatch"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.movie_releases_pt.function_name}"
  principal = "events.amazonaws.com"
  source_arn = "${aws_cloudwatch_event_rule.once_a_day.arn}"
}
