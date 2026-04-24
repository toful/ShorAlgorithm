# Shor’s Algorithm with Qiskit

[![License](https://img.shields.io/github/license/toful/ShorAlgorithm?style=plastic)](https://github.com/toful/ShorAlgorithm)

This project demonstrates **Shor’s algorithm** for integer factorization using Qiskit.

This repository provides an educational implementation of Shor’s algorithm using Qiskit, designed to illustrate the quantum period‑finding subroutine for integer factorization.

Important: This implementation is not scalable and is intended only for small composite integers (e.g., N≤21N \leq 21N≤21). It runs on a classical simulator and prioritizes clarity over performance.

You can also run the algorithm in IBM Quantum Platform, but it crashes with N > 2^3.


## How the Algorithm Works (High‑Level)

* 1-Prepare a superposition over the counting register
* 2-Apply controlled modular exponentiation:

```	
	∣y⟩ → ∣ a^x⋅y  mod N ⟩
```

* 3-Apply the inverse Quantum Fourier Transform
* 4-Measure the counting register
* 5-Use classical continued fractions to infer the period r
* 6-Compute factors via:

```
	gcd⁡(a^(r/2) ± 1, N)
```

### Limitations & Assumptions

- Only works for small N
- Assumes a is coprime with N
- Unitary modular multiplication is constructed explicitly as a matrix


## Project Structure

```
ShorAlgorithm/
│
├── README.md
├── requirements.txt
├── shor.py			Executes Shor’s algorithm from the terminal
├── shor_ibm.py			Executes Shor’s algorithm in IBM Quantum Hardware
├── notebooks/
│   └── shor_algorithm.ipynb	Jupyter Notebook with an explanation of how Shor’s algorithm works
├── src/
│   ├── __init__.py
│   └── shor_core.py		Methods for Shor’s algorithm
└── keys/
    └── ibm_quantum_key.json	Key to call the IBM Quantum Hardware
```



## Execution

Here we provide three scripts for running Shor's algorithm.

* **shor.py** -> Executes Shor’s algorithm from the terminal
* **shor_ibm.py** -> Executes Shor’s algorithm in IBM Quantum Hardware
* **shor_algorithm.ipynb** -> Jupyter Notebook with an explanation of how Shor’s algorithm works


###  Requirements

- Python ≥ 3.9
- pip

### Virtual Environment Setup

bash

	python -m venv venv
	source venv/bin/activate  # Linux / macOS
	venv\Scripts\activate     # Windows
	pip install -r requirements.txt

### Run

**shor.py**

Executes Shor’s algorithm from the terminal
Accepts:

- N: the composite number to factor
- a: a coprime integer used for order finding

Example:

	python shor.py 21 5


**shor_ibm.py**

Executes Shor’s algorithm calling the IBM Quantum Computer
Requires:

- [IBM key](https://quantum.cloud.ibm.com/)

Accepts:

- N: the composite number to factor (if its bigger than 7 it does not work with IBM)
- a: a coprime integer used for order finding

Example:

	python shor_ibm.py 6 5


**ShorAlgorithmSimulation.ipynb**

Jupyter Notebook with an explanation of how Shor’s algorithm works

	jupyter notebook notebboks/ShorAlgorithmSimulation.ipynb



## Author

* **Cristòfol Daudén Esmel** - [toful](https://github.com/toful)
