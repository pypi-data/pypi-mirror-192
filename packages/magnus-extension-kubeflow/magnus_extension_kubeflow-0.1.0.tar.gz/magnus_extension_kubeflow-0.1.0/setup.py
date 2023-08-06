# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magnus_extension_kubeflow']

package_data = \
{'': ['*']}

install_requires = \
['kfp>=1.8.18,<2.0.0', 'magnus>=0.4.1,<0.5.0']

entry_points = \
{'magnus.executor.BaseExecutor': ['kfp = '
                                  'magnus_extension_kubeflow.implementation:KubeFlowExecutor'],
 'magnus.integration.BaseIntegration': ['kfp-catalog-file_system = '
                                        'magnus_extension_kubeflow.integration:KfPComputeFileSystemCatalog',
                                        'kfp-run_log_store-buffered = '
                                        'magnus_extension_kubeflow.integration:KfPComputeBufferedRunLogStore',
                                        'kfp-run_log_store-file_system = '
                                        'magnus_extension_kubeflow.integration:KfPComputeFileSystemRunLogStore']}

setup_kwargs = {
    'name': 'magnus-extension-kubeflow',
    'version': '0.1.0',
    'description': 'Kubeflow executor',
    'long_description': '# AWS Secrets manager\n\nThis package is an extension to [magnus](https://github.com/AstraZeneca/magnus-core).\n\n## Provides \n\nProvides functionality to use Kubeflow pipelines as an Executor\n\n## Installation instructions\n\n```pip install magnus_extension_kubeflow```\n\n## Set up required to use the extension\n\n\n## Config parameters\n\nThe full configuration of the AWS secrets manager is:\n\n```yaml\nmode:\n  type: \'kfp\'\n  config:\n    docker_image: # Required\n    output_file: \'pipeline.yaml\'\n    default_cpu_limit: "250m"\n    default_memory_limit: "1G"\n    default_cpu_request:  "" # defaults to default_cpu_limit\n    default_memory_request: "" # defaults to default_memory_limit\n    enable_caching: False\n    image_pull_policy: "IfNotPresent"\n    secrets_from_k8s: null # dictionary of EnvVar=SecretName:Key\n```\n\n',
    'author': 'Vijay Vammi',
    'author_email': 'mesanthu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AstraZeneca/magnus-extensions/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
