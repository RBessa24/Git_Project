#####################################
resource "aws_ecr_repository" "rio-academy" {
  name = "my-first-ecr-repo" # Naming my repository
  image_tag_mutability = "IMMUTABLE"
}

################## Outputs ########################
output "aws_ecr_registry_id" {
  value = aws_ecr_repository.rio-academy
}

output "aws_ecr_repository_url" {
  value = aws_ecr_repository.rio-academy.repository_url
}