from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2
from src.shor_core import run_shor, classical_postprocess, build_shor_circuit
import json
from pathlib import Path
import argparse
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

"""
Loads the IBM Quantum API key from a JSON file.

Parameters
----------
json_path : str or Path
Path to the JSON file containing the API key.

Returns
-------
str
The IBM Quantum API key.
"""
def load_ibm_quantum_api_key(json_path):

    json_path = Path(json_path)

    if not json_path.exists():
        raise FileNotFoundError(f"Key file not found: {json_path}")

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if "apikey" not in data:
        raise KeyError("Missing 'apikey' field in JSON file")

    return data["apikey"]

def main():
	parser = argparse.ArgumentParser(description="Shor's algorithm using Qiskit")
	parser.add_argument("N", type=int, help="Number to factorize")
	parser.add_argument("a", type=int, help="Random integer coprime with N")
	parser.add_argument("--shots", type=int, default=1024)
	args = parser.parse_args()

	print(f"Factoring N={args.N} using a={args.a}")
	#Build the quantum circuit
	qc, n_count = build_shor_circuit(args.N, args.a)
	
	#load the apikey	
	api_key = load_ibm_quantum_api_key("keys/ibm_quantum_key.json")


	QiskitRuntimeService.save_account(token=api_key, overwrite=True)

	service = QiskitRuntimeService()
	print(service.backends())
	#select a free computer
	backend = service.least_busy(simulator=False, operational=True)

	#Compile the cicuit for run it into the IBM cimputer
	pm = generate_preset_pass_manager(target=backend.target, optimization_level=1)
	compiled_circuit = pm.run(qc)
	#compiled_circuit.draw("mpl", filename="compiled_circuit.png")
	print(compiled_circuit.draw("text"))

	#Run Execution
	sampler = SamplerV2(mode=backend)
	job=sampler.run([compiled_circuit], shots=1024)
	result = job.result()
	counts = result[0].data.c.get_counts()

	# Show the histogram
	plot_histogram(counts)
	plt.show()

	factors = classical_postprocess(counts, args.a, args.N, n_count)

	if factors:
	    print("Factors found:", factors)
	else:
	    print("No non-trivial factors found.")


if __name__ == "__main__":
    main()


