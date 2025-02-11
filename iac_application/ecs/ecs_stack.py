from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecs_patterns as ecs_patterns,
    Stack,
    CfnOutput
)

from constructs import Construct

from modules.module_ecs.ecs_cluster import EcsCluster
from modules.module_ecs.fargate_services import FargateService

class EcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)      
        
        ecs_cluster = EcsCluster(self, "EcsCluster", vpc=vpc)

        # Create a Fargate service using the reusable module
        FargateService(
            self,
            "FargateService",
            cluster=ecs_cluster.cluster,
            image="nginx:latest",
            cpu=256,
            memory_limit_mib=512,
            public_load_balancer=False
        )
    
