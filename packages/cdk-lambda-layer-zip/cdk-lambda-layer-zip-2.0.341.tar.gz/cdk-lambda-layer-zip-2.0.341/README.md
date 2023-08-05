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
