from aws_cdk import (
    Duration,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
)
from constructs import Construct

class FargateService(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        cluster: ecs.Cluster,
        cpu: int = 512,
        memory_limit_mib: int = 1024,
        desired_count: int = 1,
        image: str = "amazon/amazon-ecs-sample",
        container_port: int = 80,
        public_load_balancer: bool = False,
         **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        exec_role, container_task_role = self.ecs_policies()

        # Create a load-balanced Fargate service
        self.load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 
            "Service",
            cluster=cluster,
            memory_limit_mib=memory_limit_mib,
            desired_count=desired_count,
            cpu=cpu,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry(image),
                container_port=container_port,
                task_role=container_task_role,
                execution_role=exec_role,
                environment={
                    "ENV_VAR1": "value1",
                    "ENV_VAR2": "value2",
                    # Agrega más variables de entorno según sea necesario
                }            
            ),
            min_healthy_percent=100,
            public_load_balancer=public_load_balancer,     
        )

        # # Configure health check for the ALB
        # self.load_balanced_fargate_service.target_group.configure_health_check(
        #     path="/",  # Health check path
        #     healthy_threshold_count=2,  # Number of consecutive successful health checks
        #     unhealthy_threshold_count=3,  # Number of consecutive failed health checks
        #     timeout=Duration.seconds(5),  # Health check timeout
        #     interval=Duration.seconds(30),  # Health check interval
        # )

        # Enable auto-scaling for the Fargate service
        scalable_target = self.load_balanced_fargate_service.service.auto_scale_task_count(
            min_capacity=1,  # Minimum number of tasks
            max_capacity=10,  # Maximum number of tasks
        )
        scalable_target.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70,  # Target CPU utilization percentage
        )

    def ecs_policies(self):
      exec_role = iam.Role(
          self, 
          'MyAppTaskExecutionRole',
          assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com')
      )
      exec_role.add_managed_policy(
          iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonECSTaskExecutionRolePolicy')
      )

      container_task_role = iam.Role(
          self, 
          'MyAppTaskRole',
          assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com')
      )
      container_task_role.add_managed_policy(
                 
          iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')
      )
      container_task_role.add_managed_policy(
          iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSQSFullAccess')
      )

      return exec_role, container_task_role

    # Expose the DNS name of the load balancer as a property
    @property
    def service_dns(self) -> str:
        return self.load_balanced_fargate_service.load_balancer.load_balancer_dns_name