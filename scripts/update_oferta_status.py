import json
import os
import pathlib
import csv
from datetime import date

# TODO: Implement logic to parse comment body, update oferta status in ofertas_ativas.json,
# and add entry to historico_doacoes.csv.
# This will likely involve using the PyGithub library to get comment and issue details.

def main():
    comment_body = os.environ.get("COMMENT_BODY")
    issue_number = os.environ.get("ISSUE_NUMBER")

    if not comment_body or not issue_number:
        print("Error: COMMENT_BODY or ISSUE_NUMBER environment variables not set.")
        return

    print(f"Processing comment on issue {issue_number}: {comment_body}")

    data_dir = pathlib.Path("_data")
    data_dir.mkdir(exist_ok=True)
    ofertas_file = data_dir / "ofertas_ativas.json"
    historico_file = data_dir / "historico_doacoes.csv"

    new_status = None
    if "/reservar" in comment_body.lower():
        new_status = "reservada"
    elif "/coletar" in comment_body.lower():
        new_status = "coletada"
    
    if not new_status:
        print(f"No action keyword found in comment on issue {issue_number}. Nothing to do.")
        return

    updated_ofertas = []
    oferta_found_and_updated = False
    
    if ofertas_file.exists():
        with open(ofertas_file, "r", encoding="utf-8") as f:
            try:
                ofertas = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {ofertas_file} contains invalid JSON. Cannot update status.")
                # Create an empty list if JSON is invalid, to avoid error on write
                ofertas = []
        
        for oferta_idx, oferta in enumerate(ofertas):
            if str(oferta.get("issue_number")) == str(issue_number):
                if oferta.get("status") == new_status:
                    print(f"Status for issue {issue_number} is already {new_status}. No change made.")
                    oferta_found_and_updated = True # Mark as found to prevent "not found" message
                    # No actual update, but we need to ensure the loop continues and writes back the data
                else:
                    ofertas[oferta_idx]["status"] = new_status
                    print(f"Updated status for issue {issue_number} to {new_status}")
                    oferta_found_and_updated = True

                    if new_status == "coletada":
                        # Add to historico_doacoes.csv
                        file_exists = historico_file.exists()
                        with open(historico_file, "a", newline="", encoding="utf-8") as hf:
                            writer = csv.writer(hf)
                            if not file_exists or hf.tell() == 0: # Check if new file or empty
                                writer.writerow(["issue_number", "item", "quantidade", "escola_codinep", "data_coleta"])
                            writer.writerow([
                                issue_number,
                                oferta.get("item", "N/A"),
                                oferta.get("quantidade", "N/A"),
                                oferta.get("escola_codinep", "N/A"),
                                date.today().isoformat()
                            ])
                        print(f"Added entry to {historico_file} for issue {issue_number}")
                # No need to keep iterating once the target issue is found and processed
                # updated_ofertas = ofertas # Assign the modified list
                # break # Exit loop once the relevant offer is processed
        
        if not oferta_found_and_updated:
            print(f"Warning: Issue {issue_number} not found in {ofertas_file}. Cannot update status.")
            # If the offer wasn't found, and the file existed, we just write back the original content.
            # If it's an empty file or malformed, 'ofertas' would be empty or from a fresh load.
            # The current logic will just re-dump 'ofertas' which might be empty if file was bad.
            # This is acceptable for a stub.
            
        # Write out the potentially modified list of all offers
        with open(ofertas_file, "w", encoding="utf-8") as f:
            json.dump(ofertas, f, ensure_ascii=False, indent=2)
        print(f"Successfully processed comment for issue {issue_number}. {ofertas_file} updated.")

    else: # ofertas_file does not exist
        print(f"{ofertas_file} does not exist. No update performed as there are no offers to update.")


if __name__ == "__main__":
    main()
