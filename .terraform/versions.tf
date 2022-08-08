terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  backend "s3" {
    bucket="terraform-20220808142901786700000001"
    key="root"
    region="eu-west-1"
  }
}
