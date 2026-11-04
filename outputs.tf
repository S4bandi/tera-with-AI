output "vpc_id" {
  value = aws_vpc.main.id
}

output "subnet_id" {
  value = aws_subnet.app_subnet.id
}

output "security_group_id" {
  value = aws_security_group.web_sg.id
}

output "network_interface_id" {
  value = aws_network_interface.web_eni.id
}
