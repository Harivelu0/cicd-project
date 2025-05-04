resource "aws_instance" "hpsserver" {
  ami="ami-084568db4383264d4"
  instance_type = "t2.micro"
  subnet_id = var.sn
  security_groups = [var.sg]

  tags = {
    Name="hpserver"
  }

}