# Configure AWS provider
provider "aws" {
  region = "us-east-1"
}

# Define EC2 instance resource
resource "aws_instance" "cassandra" {
  count         = 8
  ami           = "ami-0c55b159cbfafe1f0" # Replace with Cassandra AMI
  instance_type = "t3.medium" # Replace with appropriate instance type for your workload
  key_name      = "my-keypair" # Replace with your SSH key pair name

  # Attach instance to VPC and subnet
  vpc_security_group_ids = ["${aws_security_group.cassandra.id}"]
  subnet_id              = "${aws_subnet.cassandra.id}"

  # User data script to install and configure Cassandra
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y java-1.8.0-openjdk.x86_64
              sudo rpm --import https://www.apache.org/dist/cassandra/KEYS
              echo "[datastax]
              name = DataStax Repository
              baseurl = https://rpm.datastax.com/enterprise
              enabled = 1
              gpgcheck = 0" | sudo tee -a /etc/yum.repos.d/datastax.repo
              sudo yum install -y dse-full
              EOF
}

# Define security group resource for Cassandra
resource "aws_security_group" "cassandra" {
  name_prefix = "cassandra-"
  ingress {
    from_port = 9042
    to_port   = 9042
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Define subnet resource for Cassandra
resource "aws_subnet" "cassandra" {
  cidr_block = "10.0.1.0/24" # Replace with your desired CIDR block
}

# Define VPC resource for Cassandra
resource "aws_vpc" "cassandra" {
  cidr_block = "10.0.0.0/16" # Replace with your desired CIDR block
}
