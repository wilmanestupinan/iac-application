import aws_cdk as core
import aws_cdk.assertions as assertions

from iac_application.iac_application_stack import IacApplicationStack

# example tests. To run these tests, uncomment this file along with the example
# resource in iac_application/iac_application_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = IacApplicationStack(app, "iac-application")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
