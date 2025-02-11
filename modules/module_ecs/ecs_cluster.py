from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    Stack,
)
from constructs import Construct

class EcsCluster(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vpc: ec2.Vpc,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an ECS cluster
        self.cluster = ecs.Cluster(
            self,
            "EcsCluster",
            vpc=vpc,
        )