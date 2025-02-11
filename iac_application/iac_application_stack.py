from aws_cdk import (
    # Duration,
    CfnOutput,
    Stack,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_rds as rds,
    RemovalPolicy,
)
from constructs import Construct

from iac_application import config

class IacApplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Define subnet configurations
        subnet_configurations = [
            ec2.SubnetConfiguration(
                name="PublicSubnet1",
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=24,
                map_public_ip_on_launch=True,
            ),
            ec2.SubnetConfiguration(
                name="PrivateSubnet1",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                cidr_mask=24,
            ),
        ]

        self.vpc = ec2.Vpc(
            self,
            config.VPC,
            max_azs=2,
            cidr="10.0.0.0/16",
            nat_gateways=1,
            subnet_configuration=subnet_configurations,
            enable_dns_support=True,
            enable_dns_hostnames=True,
        )

