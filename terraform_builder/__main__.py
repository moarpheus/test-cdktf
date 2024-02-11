from constructs import Construct
from cdktf import App, NamedRemoteWorkspace, TerraformStack, TerraformOutput, RemoteBackend
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance
from cdktf_cdktf_provider_aws.vpc import Vpc
from cdktf_cdktf_provider_aws.subnet import Subnet

print("Generating")

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, "AWS", region="eu-west-1")

        vpc = Vpc(self, "homedir",
                  tags={"name": "Juris"},
                  instance_tenancy="default",
                  cidr_block="10.0.0.0/16")

        subnet = Subnet(self, "homesubnet",
                        vpc_id=vpc.id,
                        cidr_block="10.0.0.0/24",
                        availability_zone="eu-west-1a",
                        depends_on=[vpc])

        instance = Instance(self, "compute",
                            ami="ami-0766b4b472db7e3b9",
                            instance_type="t2.micro",
                            subnet_id=subnet.id,
                            depends_on=[subnet]
                            )

        TerraformOutput(self, "vpc_id",
                        value=vpc.id,
                        )
        TerraformOutput(self, "subnet_id",
                        value=subnet.cidr_block,
                        )
        TerraformOutput(self, "instance_id",
                        value=instance.id,
                        )


app = App()
stack = MyStack(app, "aws_instance")
app.synth()

print("Finished")