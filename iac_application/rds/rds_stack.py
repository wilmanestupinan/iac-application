from logging import config
from aws_cdk import (
    CfnOutput,
    Stack,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_rds as rds,
    RemovalPolicy,
)
from constructs import Construct

class RDSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc=ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        db_security_group = ec2.SecurityGroup(
            self,
            "DatabaseSecurityGroup",
            vpc=vpc,
            description="Security group for the database",
            allow_all_outbound=True,  # Allow outbound traffic
        )

        # Allow inbound traffic to the database (e.g., from the application)
        db_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("10.0.0.0/16"),  # Allow traffic from within the VPC
            connection=ec2.Port.tcp(5432),  # Postgres/Aurora default port
            description="Allow Postgres traffic from within the VPC",
        )

        # Create an RDS database instance in the private subnet
        database = rds.DatabaseInstance(
            self,
            "RDS-XYZ",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_16_6
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.R5,
                ec2.InstanceSize.LARGE,
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS  # Place the database in private subnets
            ),
            security_groups=[db_security_group],
            removal_policy=RemovalPolicy.DESTROY,  # Destroy the database when the stack is deleted
            deletion_protection=False,  # Allow deletion of the database
            database_name="dbdojoxyz",  # Name of the database
            credentials=rds.Credentials.from_generated_secret(
                "dojo_user"
            ),  # Generate a secret for the admin user
        )

        # Output the database endpoint
        self.output_database_endpoint(database)

    def output_database_endpoint(self, database):
        """Output the database endpoint for easy access."""
        ssm.StringParameter(
            self,
            "DatabaseEndpoint",
            parameter_name="/dogo/database/endpoint",
            string_value=database.db_instance_endpoint_address,
        )