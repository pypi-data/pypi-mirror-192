# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src', 'simulator': 'src/simulator'}

packages = \
['quantuloop', 'quantuloop.simulator', 'simulator']

package_data = \
{'': ['*']}

install_requires = \
['quantuloop-dense>=0.1.0,<0.2.0',
 'quantuloop-quest>=0.1.3,<0.2.0',
 'quantuloop-sparse>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'quantuloop-simulator',
    'version': '2023.2.dev1',
    'description': 'Quantuloop Quantum Simulator Suite for HPC',
    'long_description': '# Quantuloop Quantum Simulator Suite for HPC\n\nThe Quantuloop Quantum Simulator Suite for HPC is a collection of high-performance quantum computer simulators for the [Ket](https://quantumket.org) language. Since quantum algorithms explore distinct aspects of quantum computation to extract advantages, there is no silver bullet for the simulation of a quantum computer. The Quantuloop Quantum Simulator Suite for HPC offers three quantum simulators today, with new ones coming in the future. The simulator available today are:\n\n* **Quantuloop Sparse** brings the Bitwise Representation (implemented in the KBW Sparse) for HPC.\n  * Ready for muti-GPU systems.\n  * Execution time O(s log(s)) with the amount of superposition (s).\n  * Exact simulation of more than 100 qubits [depending on the algorithm](https://repositorio.ufsc.br/handle/123456789/231060).\n* **Quantuloop Dense** state vector simulator built with the NVIDIA cuQuantum SDK cuStateVec.\n  * Great scalability in multi-GPU systems\n  * The perfect fit for most quantum algorithms.\n* **Quantuloop QuEST** is an interface for the open-source simulator QuEST.\n  * Excellent performance for single GPU systems.\n\nThe use of this simulator is exclusively for Quantuloop\'s customers and partners. Contact your institution to get your access token or visit <https://quantuloop.com.br>.\n\n## Installation  \n\nInstalling using pip:\n\n```shell\npip install --index-url https://gitlab.com/api/v4/projects/43029789/packages/pypi/simple quantuloop-simulator\n```\n\nAdd in poetry:\n\n```shell\npoetry source add quntuloop https://gitlab.com/api/v4/projects/43029789/packages/pypi/simple --secondary\npoetry add quantuloop-simulator\n```\n\n## Usage\n\n```py\nimport quantuloop.simulator as ql\n\nql.set_token("YOR.ACCESS.TOKEN") # a Quantuloop access token is required to use the simulators \n\n# Select the simulator\nql.use_sparse() # Quantuloop Sparse\nql.use_dense()  # Quantuloop Dense \nql.use_quest()  # Quantuloop QuEST\n\n# Sets the floating point precision\nql.set_precision(1) # single precision (default) \nql.set_precision(2) # double precision (not available in QuEST)\n\n# Sets the maximum number of GPUs\nql.set_gpu_count(4) # use all GPUs by default\n```\n\n## Compatibility\n\n* CUDA 11.2 or newer with compatible NVIDIA driver\n* Linux x86_64 with glibc 2.17 or newer\n  * Ubuntu 18.04 or newer.\n  * Red Hat Enterprise Linux 7 or newer.\n* Python 3.7 or newer\n* Ket 0.5.x\n\nQuantuloop Dense is compatible only with CUDA architecture 70, 75, 80, and 86.\n\n----\n\nBy installing or using this package, you agree to the Quantuloop Quantum Simulator Suite EULA.\n\nAll rights reserved (C) 2023 Quantuloop\n',
    'author': 'Quantuloop',
    'author_email': 'contact@quantuloop.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
