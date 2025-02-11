from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_ec2 as ec2,
    aws_ssm as ssm,
)
NAME_PROYECT = "iac-dojo"
# basic VPC configs
VPC = f"{NAME_PROYECT}-vpc"

INTERNET_GATEWAY = f"{NAME_PROYECT}internet-gateway"
NAT_GATEWAY = f"{NAME_PROYECT}-nat-gateway"
REGION = "us-east-1"

# route tables
PUBLIC_ROUTE_TABLE = f"{NAME_PROYECT}-public-route-table"
PRIVATE_ROUTE_TABLE = f"{NAME_PROYECT}-private-route-table"

ROUTE_TABLES_ID_TO_ROUTES_MAP = {
    PUBLIC_ROUTE_TABLE: [
        {
            "destination_cidr_block": "0.0.0.0/0",
            "gateway_id": INTERNET_GATEWAY,
            "router_type": ec2.RouterType.GATEWAY,
        }
    ],
    PRIVATE_ROUTE_TABLE: [
        {
            "destination_cidr_block": "0.0.0.0/0",
            "nat_gateway_id": NAT_GATEWAY,
            "router_type": ec2.RouterType.NAT_GATEWAY,
        }
    ],
}

# subnets and instances
PUBLIC_SUBNET_1 = f"{NAME_PROYECT}-public-subnet-1"
PUBLIC_SUBNET_2 = f"{NAME_PROYECT}-public-subnet-2"
PRIVATE_SUBNET_1 = f"{NAME_PROYECT}-private-subnet-1"
PRIVATE_SUBNET_2 = f"{NAME_PROYECT}-private-subnet-2"

PUBLIC_INSTANCE = f"{NAME_PROYECT}-public-instance"
PRIVATE_INSTANCE = f"{NAME_PROYECT}-private-instance"


SUBNET_CONFIGURATION = {
    PUBLIC_SUBNET_1: {
        "availability_zone": "us-east-1a",
        "cidr_block": "10.0.1.0/24",
        "map_public_ip_on_launch": True,
        "route_table_id": PUBLIC_ROUTE_TABLE
    },
    PUBLIC_SUBNET_2: {
        "availability_zone": "us-east-1b",
        "cidr_block": "10.0.2.0/24",
        "map_public_ip_on_launch": True,
        "route_table_id": PUBLIC_ROUTE_TABLE
    },
    PRIVATE_SUBNET_1: {
        "availability_zone": "us-east-1a",
        "cidr_block": "10.0.10.0/24",
        "map_public_ip_on_launch": False,
        "route_table_id": PRIVATE_ROUTE_TABLE
    },
    PRIVATE_SUBNET_2: {
        "availability_zone": "us-east-1b",
        "cidr_block": "10.0.11.0/24",
        "map_public_ip_on_launch": False,
        "route_table_id": PRIVATE_ROUTE_TABLE
    },
}
