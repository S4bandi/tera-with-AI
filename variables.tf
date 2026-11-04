variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
}

variable "environment" {
  description = "Enviroment name such as dev or prod"
  type        = string
}


variable "my_ip" {
  description = "Allowed IP CIDR for SSH access"
  type        = string
}

