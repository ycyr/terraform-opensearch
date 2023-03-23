terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-east-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-02f3f602d23f1659d"
  instance_type = "t2.micro"

  tags = {
    Name = "ExampleAppServerInstance"
  }
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}


resource "aws_security_group" "allow_opensearch" {
  name        = "allow_opensearch"
  description = "Allow TLS inbound opensearch"
  vpc_id      = aws_default_vpc.default.id

  ingress {
    description      = "Opensearch TLS from VPC"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks  = ["0.0.0.0/0"]
   
  }


  tags = {
    Name = "allow_opensearch"
  }
}
