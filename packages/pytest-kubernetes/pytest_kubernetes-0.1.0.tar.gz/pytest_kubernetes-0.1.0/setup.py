# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_kubernetes', 'pytest_kubernetes.providers']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0', 'pyyaml>=6.0,<7.0']

entry_points = \
{'pytest11': ['pytest-kubernetes = pytest_kubernetes.plugin']}

setup_kwargs = {
    'name': 'pytest-kubernetes',
    'version': '0.1.0',
    'description': '',
    'long_description': '# pytest-kubernetes\npytest-kubernetes is a lightweight pytest plugin that makes managing (local) Kubernetes clusters a breeze. You can easily spin up a Kubernetes cluster with one [pytest fixure](https://docs.pytest.org/en/latest/explanation/fixtures.html) and remove them again.\nThe fixture comes with some simple functions to interact with the cluster, for example `kubectl(...)` that allows you to run typical *kubectl* commands against this cluster without worring \nabout the *kubeconfig* on the test machine.\n\n**Features:**\n- Set up and tear down (local) Kubernetes clusters with *minikube*, *k3d* and *kind*\n- Configure the cluster to recreate for each test case (default), or keep it across multiple test cases\n- Automatic management of the *kubeconfig*\n- Simple functions to run kubectl commands (with *dict* output), reading logs and load custom container images\n- Management utils for custom pytest-fixtures (for example pre-provisioned clusters)\n \n## Installation\nThis plugin can be installed from PyPI:\n- `pip install pytest-kubernetes`\n- `poetry add -D pytest-kubernetes`\n\nNote that this package provides entrypoint hooks to be automatically loaded with pytest.\n\n## Requirements\npytest-kubernetes expects the following components to be available on the test machine:\n- [`kubectl`](https://kubernetes.io/docs/reference/kubectl/)\n- [`minikube`](https://minikube.sigs.k8s.io/docs/start/) (optional for minikube-based clusters)\n- [`k3d`](https://k3d.io/) (optional for k3d-based clusters)\n- [`kind`](https://kind.sigs.k8s.io/) (optional for kind-based clusters)\n- [Docker](https://docs.docker.com/get-docker/) (optional for Docker-based Kubernetes clusters)\n\nPlease make sure they are installed to run pytest-kubernetes properly.\n\n## Reference\n\n### Fixture\n\n#### k8s\nThe _k8s_ fixture provides access to an automatically selected Kubernetes provider (depending on the availability on the host). The priority is: k3d, kind, minikube-docker and minikube-kvm2.\n\nThe fixture passes a manager object of type *AClusterManager*.\nIt provides the following interface:\n- *kubectl(...)*: Execute kubectl command against this cluster\n- *apply(...)*: Apply resources to this cluster, either from YAML file, or Python dict\n- *load_image(...)*: Load a container image into this cluster\n- *logs(...)*: Get the logs of a pod\n- *version()*: Get the Kubernetes version of this cluster\n- *create(...)*: Create this cluster\n- *delete()*: Delete this cluster\n- *reset()*: Delete this cluster (if it exists) and create it again\n\nThe interface provides proper typing and should be easy to work with.\n\n**Example**\n\n```python\ndef test_a_feature_with_k3d(k8s: AClusterManager):\n    k8s.create()\n    k8s.apply(\n        {\n            "apiVersion": "v1",\n            "kind": "ConfigMap",\n            "data": {"key": "value"},\n            "metadata": {"name": "myconfigmap"},\n        },\n    )\n    k8s.apply("./dependencies.yaml")\n    k8s.load_image("my-container-image:latest")\n    k8s.kubectl(\n        [\n            "run",\n            "test",\n            "--image",\n            "my-container-image:latest",\n            "--restart=Never",\n            "--image-pull-policy=Never",\n        ]\n    )\n```\nThis cluster will be deleted once the test case is over.\n\n> Please note that you need to set *"--image-pull-policy=Never"* for images that you loaded into the cluster via the `k8s.load(name: str)` function (see example above).\n\n### Marks\npytest-kubernetes uses [*pytest marks*](https://docs.pytest.org/en/7.1.x/how-to/mark.html) for specifying the cluster configuration for a test case\n\nCurrently the following settings are supported:\n\n- *provider* (str): request a specific Kubernetes provider for the test case \n- cluster_name (str): request a specific cluster name\n- keep (bool): keep the cluster across multiple test cases\n\n**Example**\n```python\n@pytest.mark.k8s(provider="minikube", cluster_name="test1", keep=True)\ndef test_a_feature_in_minikube(k8s: AClusterManager):\n    ...\n```\n\n## Examples\nPlease find more examples in *tests/vendor.py* in this repository. These test cases are written as you would write test cases in your project.',
    'author': 'Michael Schilonka',
    'author_email': 'michael@blueshoe.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
