import aws_cdk as cdk
import os

from iac_application.ecs.ecs_stack import EcsStack
from iac_application.iac_application_stack import IacApplicationStack
from iac_application.rds.rds_stack import RDSStack

env = cdk.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT', '767397670732'),
    region=os.getenv('CDK_DEFAULT_REGION', 'us-east-1')
)

app = cdk.App()
vpc_stack = IacApplicationStack(
    app, 
    "IacApplicationStack",
    env=env
    )

EcsStack(
    app, 
    "EcsStack", 
    vpc=vpc_stack.vpc,
    env=env
)

# RDSStack( app, 
#     "RDSStack", 
#     vpc=vpc_stack.vpc,
#     env=env
# )

app.synth()
