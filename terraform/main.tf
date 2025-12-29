terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# This Terraform scaffold is intentionally minimal to keep demo costs low.
# Recommended approach:
# - Use local FAISS mode for demos
# - Add OpenSearch / Bedrock components as needed for real deployment
