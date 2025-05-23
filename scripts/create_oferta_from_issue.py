# JSON Schema for _data/ofertas_ativas.json
# [
#   {
#     "issue_number": "string",
#     "escola_codinep": "string",
#     "item": "string",
#     "quantidade": "string",
#     "validade": "string",
#     "observacoes": "string",
#     "status": "string" // e.g., "disponivel", "reservada", "coletada"
#   }
# ]
import json
import os
import pathlib

# TODO: Implement logic to read issue details and create/update ofertas_ativas.json
# This will likely involve using the PyGithub library to interact with GitHub issues.

def main():
    issue_number = os.environ.get("ISSUE_NUMBER")
    if not issue_number:
        print("Error: ISSUE_NUMBER environment variable not set.")
        return

    print(f"Processing issue number: {issue_number}")

    # Placeholder for data to be written to ofertas_ativas.json
    # This should be populated based on the issue details
    oferta_data = {
        "issue_number": issue_number,
        "escola_codinep": "TODO",
        "item": "TODO",
        "quantidade": "TODO",
        "validade": "TODO",
        "observacoes": "TODO",
        "status": "disponivel" # Initial status
    }

    data_dir = pathlib.Path("_data")
    data_dir.mkdir(exist_ok=True)
    ofertas_file = data_dir / "ofertas_ativas.json"

    ofertas = []
    if ofertas_file.exists():
        with open(ofertas_file, "r", encoding="utf-8") as f:
            try:
                ofertas = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {ofertas_file} contains invalid JSON. Starting with an empty list.")
                ofertas = []
    
    # Add or update the offer
    # For simplicity, this placeholder currently just appends.
    # A real implementation would need to check if the offer (by issue_number) already exists and update it.
    ofertas.append(oferta_data)

    with open(ofertas_file, "w", encoding="utf-8") as f:
        json.dump(ofertas, f, ensure_ascii=False, indent=2)

    print(f"Successfully processed issue {issue_number} and updated {ofertas_file}")

if __name__ == "__main__":
    main()
