'''
# AWS Lambda Layer with zip

[![NPM version](https://badge.fury.io/js/cdk-lambda-layer-zip.svg)](https://badge.fury.io/js/cdk-lambda-layer-zip)
[![PyPI version](https://badge.fury.io/py/cdk-lambda-layer-zip.svg)](https://badge.fury.io/py/cdk-lambda-layer-zip)
![Release](https://github.com/clarencetw/cdk-lambda-layer-zip/workflows/release/badge.svg)
[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/clarencetw/cdk-lambda-layer-zip)

Usage:

```python
// ZipLayer bundles the tar gzip 7z in a lambda layer
import { ZipLayer } from 'cdk-lambda-layer-zip';

declare const fn: lambda.Function;
fn.addLayers(new ZipLayer(this, 'ZipLayer'));
```

```python
import { ZipLayer } from 'cdk-lambda-layer-zip'
import * as lambda from 'aws-cdk-lib/aws-lambda'

new lambda.Function(this, 'MyLambda', {
  code: lambda.Code.fromAsset(path.join(__dirname, 'my-lambda-handler')),
  handler: 'index.main',
  runtime: lambda.Runtime.PYTHON_3_9,
  layers: [new ZipLayer(this, 'ZipLayer')]
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


class ZipLayer(
    _aws_cdk_aws_lambda_ceddda9d.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-layer-zip.ZipLayer",
):
    '''An AWS Lambda layer that includes the tar gzip 7z.'''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0d03df41542579a2c6826c6be55e4eb49ba1688be2308fb12748f911881ab5e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])


__all__ = [
    "ZipLayer",
]

publication.publish()

def _typecheckingstub__d0d03df41542579a2c6826c6be55e4eb49ba1688be2308fb12748f911881ab5e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
