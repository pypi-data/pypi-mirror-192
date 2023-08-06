# Quantuloop Quantum Simulator Suite for HPC

The Quantuloop Quantum Simulator Suite for HPC is a collection of high-performance quantum computer simulators for the [Ket](https://quantumket.org) language. Since quantum algorithms explore distinct aspects of quantum computation to extract advantages, there is no silver bullet for the simulation of a quantum computer. The Quantuloop Quantum Simulator Suite for HPC offers three quantum simulators today, with new ones coming in the future. The simulator available today are:

* **Quantuloop Sparse** brings the Bitwise Representation (implemented in the KBW Sparse) for HPC.
  * Ready for muti-GPU systems.
  * Execution time O(s log(s)) with the amount of superposition (s).
  * Exact simulation of more than 100 qubits [depending on the algorithm](https://repositorio.ufsc.br/handle/123456789/231060).
* **Quantuloop Dense** state vector simulator built with the NVIDIA cuQuantum SDK cuStateVec.
  * Great scalability in multi-GPU systems
  * The perfect fit for most quantum algorithms.
* **Quantuloop QuEST** is an interface for the open-source simulator QuEST.
  * Excellent performance for single GPU systems.

The use of this simulator is exclusively for Quantuloop's customers and partners. Contact your institution to get your access token or visit <https://quantuloop.com.br>.

## Installation  

Installing using pip:

```shell
pip install --index-url https://gitlab.com/api/v4/projects/43029789/packages/pypi/simple quantuloop-simulator
```

Add in poetry:

```shell
poetry source add quntuloop https://gitlab.com/api/v4/projects/43029789/packages/pypi/simple --secondary
poetry add quantuloop-simulator
```

## Usage

```py
import quantuloop.simulator as ql

ql.set_token("YOR.ACCESS.TOKEN") # a Quantuloop access token is required to use the simulators 

# Select the simulator
ql.use_sparse() # Quantuloop Sparse
ql.use_dense()  # Quantuloop Dense 
ql.use_quest()  # Quantuloop QuEST

# Sets the floating point precision
ql.set_precision(1) # single precision (default) 
ql.set_precision(2) # double precision (not available in QuEST)

# Sets the maximum number of GPUs
ql.set_gpu_count(4) # use all GPUs by default
```

## Compatibility

* CUDA 11.2 or newer with compatible NVIDIA driver
* Linux x86_64 with glibc 2.17 or newer
  * Ubuntu 18.04 or newer.
  * Red Hat Enterprise Linux 7 or newer.
* Python 3.7 or newer
* Ket 0.5.x

Quantuloop Dense is compatible only with CUDA architecture 70, 75, 80, and 86.

----

By installing or using this package, you agree to the Quantuloop Quantum Simulator Suite EULA.

All rights reserved (C) 2023 Quantuloop
