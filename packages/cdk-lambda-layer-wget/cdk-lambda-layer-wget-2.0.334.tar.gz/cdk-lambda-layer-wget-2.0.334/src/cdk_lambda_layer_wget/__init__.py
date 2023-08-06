'''
# AWS Lambda Layer with wget

[![NPM version](https://badge.fury.io/js/cdk-lambda-layer-wget.svg)](https://badge.fury.io/js/cdk-lambda-layer-wget)
[![PyPI version](https://badge.fury.io/py/cdk-lambda-layer-wget.svg)](https://badge.fury.io/py/cdk-lambda-layer-wget)
![Release](https://github.com/clarencetw/cdk-lambda-layer-wget/workflows/release/badge.svg)
[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/clarencetw/cdk-lambda-layer-wget)

Usage:

```python
// WgetLayer bundles the wget in a lambda layer
import { WgetLayer } from 'cdk-lambda-layer-wget';

declare const fn: lambda.Function;
fn.addLayers(new WgetLayer(this, 'WgetLayer'));
```

```python
import { WgetLayer } from 'cdk-lambda-layer-wget'
import * as lambda from 'aws-cdk-lib/aws-lambda'

new lambda.Function(this, 'MyLambda', {
  code: lambda.Code.fromAsset(path.join(__dirname, 'my-lambda-handler')),
  handler: 'index.main',
  runtime: lambda.Runtime.PYTHON_3_9,
  layers: [new WgetLayer(this, 'WgetLayer')]
});
```
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

import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class WgetLayer(
    _aws_cdk_aws_lambda_ceddda9d.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-layer-wget.WgetLayer",
):
    '''An AWS Lambda layer that includes the wget.'''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0931072c0e59e7f830f767242da2fc67a23ae3751a44b5c656c9194ca866e913)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])


__all__ = [
    "WgetLayer",
]

publication.publish()

def _typecheckingstub__0931072c0e59e7f830f767242da2fc67a23ae3751a44b5c656c9194ca866e913(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
