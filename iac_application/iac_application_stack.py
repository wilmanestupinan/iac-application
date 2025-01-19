from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_ssm as ssm
)
from constructs import Construct

from module_vpc import config
from module_vpc.module_vpc import ModuleVpc


class IacApplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        self.vpc_module = ModuleVpc(self, config.VPC)

        vpc = self.vpc_module.vpc
       