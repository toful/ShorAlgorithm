import argparse
from src.shor_core import run_shor, classical_postprocess, build_shor_circuit

def main():
    parser = argparse.ArgumentParser(description="Shor's algorithm using Qiskit")
    parser.add_argument("N", type=int, help="Number to factorize")
    parser.add_argument("a", type=int, help="Random integer coprime with N")
    parser.add_argument("--shots", type=int, default=1024)
    args = parser.parse_args()

    print(f"Factoring N={args.N} using a={args.a}")
    counts, n_count, qc = run_shor(args.N, args.a, args.shots)
    factors = classical_postprocess(counts, args.a, args.N, n_count)

    if factors:
        print("Factors found:", factors)
    else:
        print("No non-trivial factors found.")
         
    
    answer = input("\nDo you want to print the generated circuit? (y/n): ").strip().lower()

    if answer in {"y", "yes", "Y", "YES"}:
        print("\nQuantum Circuit:\n")
        print(qc.draw("text"))
        qc.draw("mpl", filename="shor_circuit_N-"+str(args.N)+".png")


if __name__ == "__main__":
    main()
