output "public_sn" {
  value = aws_subnet.public_sn.id
}
output "sg" {
  value = aws_security_group.sg.id
}