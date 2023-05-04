terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>4.16"
    }
  }


  required_version = ">= 1.2.0"
}


provider "aws" {
  version = "~>4.0"
  region     = var.aws_region
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
}

#####################################
resource "aws_ecr_repository" "rio-academy" {
  name = "my-first-ecr-repo" # Naming my repository
  image_tag_mutability = "IMMUTABLE"
    image_scanning_configuration {                            # Added after checkov analysis
    scan_on_push = true
  } 
  encryption_configuration {                                # Added after checkov analysis
    encryption_type                 = "KMS"                   
  }
  force_delete                    = true
}

################## Outputs ########################
output "aws_ecr_registry_id" {
  value = aws_ecr_repository.rio-academy
}

output "aws_ecr_repository_url" {
  value = aws_ecr_repository.rio-academy.repository_url
}


########## Variables #########
variable "aws_access_key_id" {}
variable "aws_secret_access_key" {}

variable "aws_region" {
  description = "AWS Region"
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment Environment"
  default     = "testing"
}