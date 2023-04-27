terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~>2.20.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

# Declare o provedor AWS e configure suas credenciais
provider "aws" {
  region = "us-east-1"
}

# Crie a VPC
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "my-vpc"
  }
}


################ CRIAÇÃO DAS SUBREDES ####################

# Crie as sub-redes na VPC
resource "aws_subnet" "public_sub_a" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-sub-a"
  }
}

resource "aws_subnet" "private_sub_a" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false
  tags = {
    Name = "private-sub-a"
  }
}

resource "aws_subnet" "public_sub_b" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.3.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-sub-b"
  }
}

resource "aws_subnet" "private_sub_b" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.4.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = false
  tags = {
    Name = "private-sub-b"
  }
}



################ CRIAÇÃO DO IGW ####################

resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id
  tags = {
    Name = "my-igw"
  }
}

################ CRIAÇÃO DO EIP ####################
resource "aws_eip" "nat_eip_a" {
  vpc = true
}

resource "aws_eip" "nat_eip_b" {
  vpc = true
}

################ CONFIGURAÇÕES ROUTING Publicas ###############

# Adicione uma rota para o Internet Gateway na tabela de roteamento da sub-rede pública
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.my_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my_igw.id
  }

  tags = {
    Name = "public-route-table"
  }
}

# Associe a tabela de roteamento pública à sub-rede pública A
resource "aws_route_table_association" "public_subnet_association_a" {
  subnet_id      = aws_subnet.public_sub_a.id
  route_table_id = aws_route_table.public_route_table.id
}

# Associe a tabela de roteamento pública à sub-rede pública B
resource "aws_route_table_association" "public_subnet_association_b" {
  subnet_id      = aws_subnet.public_sub_b.id
  route_table_id = aws_route_table.public_route_table.id
}

# Criar tabelas de roteamento privadas para cada sub-rede privada

# Sub-rede privada A
resource "aws_route_table" "private_route_table_a" {
  vpc_id = aws_vpc.my_vpc.id

  tags = {
    Name = "private-route-table-a"
  }
}

# Sub-rede privada B
resource "aws_route_table" "private_route_table_b" {
  vpc_id = aws_vpc.my_vpc.id

  tags = {
    Name = "private-route-table-b"
  }
}

# Associar as sub-redes privadas às tabelas de roteamento privadas correspondentes

# Sub-rede privada A
resource "aws_route_table_association" "private_subnet_association_a" {
  subnet_id      = aws_subnet.private_sub_a.id
  route_table_id = aws_route_table.private_route_table_a.id
}

# Sub-rede privada B
resource "aws_route_table_association" "private_subnet_association_b" {
  subnet_id      = aws_subnet.private_sub_b.id
  route_table_id = aws_route_table.private_route_table_b.id
}




################ CRIAÇÃO DO NAT GATEWAYS ####################

# Criar dois NAT Gateways
resource "aws_nat_gateway" "nat_gateway_a" {
  allocation_id = aws_eip.nat_eip_a.id
  subnet_id     = aws_subnet.public_sub_a.id
}

resource "aws_nat_gateway" "nat_gateway_b" {
  allocation_id = aws_eip.nat_eip_b.id
  subnet_id     = aws_subnet.public_sub_b.id
}


# Criar rotas para as sub-redes privadas apontando para os NAT Gateways correspondentes
resource "aws_route" "private_route_a" {
  route_table_id         = aws_route_table.private_route_table_a.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_gateway_a.id
}

resource "aws_route" "private_route_b" {
  route_table_id         = aws_route_table.private_route_table_b.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_gateway_b.id
}




#####################################
resource "aws_ecr_repository" "rio-academy" {
  name = "my-first-ecr-repo" # Naming my repository
  image_tag_mutability = "IMMUTABLE"
}


