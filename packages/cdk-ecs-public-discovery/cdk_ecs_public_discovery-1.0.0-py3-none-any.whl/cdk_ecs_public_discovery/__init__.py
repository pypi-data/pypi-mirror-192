'''
# ECS Public Discovery

The poor man's alternative to the recommended approach of using an ELB for public ingress into your ECS service.

The provided CDK construct offers similar functionality to what AWS provides through ECS Service Discovery (also known
as AWS Cloud Map), but instead of creating a DNS entry with the private IP address of the task (even with a public Cloud
Map namespace), it will register the public IP address of the task.

This can support services with multiple tasks with Route53 multivalue answer routing.

## Installation

### TypeScript / JavaScript

`npm install cdk-ecs-public-discovery`

or

`yarn add cdk-ecs-public-discovery`

### Python

`pip install cdk-ecs-public-discovery`

### Java

```xml
<dependency>
    <groupId>com.engineal.cdk</groupId>
    <artifactId>ecs-public-discovery</artifactId>
</dependency>
```

### C# / .Net

`dotnet add package EngineAL.CDK.EcsPublicDiscovery`

## Usage

Create a new `EcsPublicDiscovery` construct for your ECS cluster. Provide the Route53 Hosted Zone to create DNS entries
in.

```python
const cluster = new ecs.Cluster(stack, 'TestCluster');
const hostedZone = route53.HostedZone.fromHostedZoneAttributes(stack, 'HostedZone', {
    hostedZoneId: 'Z1R8UBAEXAMPLE',
    zoneName: 'example.com'
});

const ecsPublicDiscovery = new EcsPublicDiscovery(stack, 'EcsPublicDiscovery', {
    cluster,
    hostedZone
});
```

Then for each service you create in that cluster that you want to enable public routing to, set `assignPublicIp` to
`true` and register it with the `EcsPublicDiscovery` construct you created:

```python
const taskDefinition = new ecs.FargateTaskDefinition(stack, 'TestTaskDefinition');

taskDefinition.addContainer('TestContainer', {
    image: ecs.ContainerImage.fromRegistry('hello-world')
});

const service = new ecs.FargateService(stack, 'TestService', {
    assignPublicIp: true,
    cluster,
    taskDefinition
});

ecsPublicDiscovery.addService({
    // eslint-disable-next-line no-magic-numbers
    dnsTtl: cdk.Duration.minutes(1),
    name: 'test',
    service
});
```

## Details

This construct creates a Lambda function that is triggered by an EventBridge rule that listens for when an ECS task is
running or has stopped.

Each ECS service registered with this construct is tagged with the `public-discovery:name` and optionally the
`public-discovery:ttl` tags based on the props you provide, which will be propagated to the service's tasks and the
network interface attached to the task. The ECS task definition must use the AwsVpc network mode, and the ECS service
must assign a public IP to its tasks' network interface.

When a task is running, the Lambda function will call the EC2 `DescribeNetworkInterfaces` API action to describe the
task's network interface to look up the public IP address and tags assigned to the task. It will then call the
Route53 `ChangeResourceRecordSets` API action to upsert an A record, using the public IP address as the value of the
resource record, the value of the `public-discovery:name` tag as the name, the value of the `public-discovery:ttl` tag
as the TTL if present or 60 seconds if absent, and the task's id as the set identifier to allow for multivalue routing.

When the task has stopped, the Lambda function will call the Route53 `ListResourceRecordSets` API action to look up the
resource record set for the task's id and will then call the Route53 `ChangeResourceRecordSets` API action to delete
that A record.

### Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run package` generates libraries for all languages
* `npm run test`    perform the jest unit tests

## License

Copyright 2023 Aaron Lucia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

```
   http://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk
import aws_cdk.aws_ecs
import aws_cdk.aws_lambda
import aws_cdk.aws_route53
import constructs


class EcsPublicDiscovery(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-ecs-public-discovery.EcsPublicDiscovery",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        hosted_zone: aws_cdk.aws_route53.IHostedZone,
        tracing: typing.Optional[aws_cdk.aws_lambda.Tracing] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: (experimental) The ECS cluster to enable ECS public discovery for.
        :param hosted_zone: (experimental) The Route 53 hosted zone to create DNS entries in.
        :param tracing: (experimental) Enable AWS X-Ray Tracing for Lambda Functions. Default: Tracing.Disabled

        :stability: experimental
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                cluster: aws_cdk.aws_ecs.ICluster,
                hosted_zone: aws_cdk.aws_route53.IHostedZone,
                tracing: typing.Optional[aws_cdk.aws_lambda.Tracing] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcsPublicDiscoveryProps(
            cluster=cluster, hosted_zone=hosted_zone, tracing=tracing
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addService")
    def add_service(
        self,
        *,
        name: builtins.str,
        service: aws_cdk.aws_ecs.BaseService,
        dns_ttl: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param name: (experimental) A name for the Service.
        :param service: (experimental) The ECS service to create DNS entries for.
        :param dns_ttl: (experimental) The amount of time that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)

        :stability: experimental
        '''
        options = ServiceOptions(name=name, service=service, dns_ttl=dns_ttl)

        return typing.cast(None, jsii.invoke(self, "addService", [options]))


@jsii.data_type(
    jsii_type="cdk-ecs-public-discovery.EcsPublicDiscoveryProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "hosted_zone": "hostedZone",
        "tracing": "tracing",
    },
)
class EcsPublicDiscoveryProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        hosted_zone: aws_cdk.aws_route53.IHostedZone,
        tracing: typing.Optional[aws_cdk.aws_lambda.Tracing] = None,
    ) -> None:
        '''
        :param cluster: (experimental) The ECS cluster to enable ECS public discovery for.
        :param hosted_zone: (experimental) The Route 53 hosted zone to create DNS entries in.
        :param tracing: (experimental) Enable AWS X-Ray Tracing for Lambda Functions. Default: Tracing.Disabled

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                cluster: aws_cdk.aws_ecs.ICluster,
                hosted_zone: aws_cdk.aws_route53.IHostedZone,
                tracing: typing.Optional[aws_cdk.aws_lambda.Tracing] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "hosted_zone": hosted_zone,
        }
        if tracing is not None:
            self._values["tracing"] = tracing

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        '''(experimental) The ECS cluster to enable ECS public discovery for.

        :stability: experimental
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_ecs.ICluster, result)

    @builtins.property
    def hosted_zone(self) -> aws_cdk.aws_route53.IHostedZone:
        '''(experimental) The Route 53 hosted zone to create DNS entries in.

        :stability: experimental
        '''
        result = self._values.get("hosted_zone")
        assert result is not None, "Required property 'hosted_zone' is missing"
        return typing.cast(aws_cdk.aws_route53.IHostedZone, result)

    @builtins.property
    def tracing(self) -> typing.Optional[aws_cdk.aws_lambda.Tracing]:
        '''(experimental) Enable AWS X-Ray Tracing for Lambda Functions.

        :default: Tracing.Disabled

        :stability: experimental
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[aws_cdk.aws_lambda.Tracing], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsPublicDiscoveryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-ecs-public-discovery.ServiceOptions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "service": "service", "dns_ttl": "dnsTtl"},
)
class ServiceOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        service: aws_cdk.aws_ecs.BaseService,
        dns_ttl: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param name: (experimental) A name for the Service.
        :param service: (experimental) The ECS service to create DNS entries for.
        :param dns_ttl: (experimental) The amount of time that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                name: builtins.str,
                service: aws_cdk.aws_ecs.BaseService,
                dns_ttl: typing.Optional[aws_cdk.Duration] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument dns_ttl", value=dns_ttl, expected_type=type_hints["dns_ttl"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "service": service,
        }
        if dns_ttl is not None:
            self._values["dns_ttl"] = dns_ttl

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) A name for the Service.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> aws_cdk.aws_ecs.BaseService:
        '''(experimental) The ECS service to create DNS entries for.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(aws_cdk.aws_ecs.BaseService, result)

    @builtins.property
    def dns_ttl(self) -> typing.Optional[aws_cdk.Duration]:
        '''(experimental) The amount of time that you want DNS resolvers to cache the settings for this record.

        :default: Duration.minutes(1)

        :stability: experimental
        '''
        result = self._values.get("dns_ttl")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EcsPublicDiscovery",
    "EcsPublicDiscoveryProps",
    "ServiceOptions",
]

publication.publish()
