import json
import os
import sys
import pathlib
from datetime import datetime
# Assuming utils.py is in the same directory or PYTHONPATH is set up
try:
    import utils
except ImportError:
    # Adjust path if running script directly and utils.py is in the same directory
    sys.path.append(str(pathlib.Path(__file__).parent.resolve()))
    import utils

# --- Configuration ---
DATA_DIR = pathlib.Path("_data")
OFERTAS_ATIVAS_FILE = DATA_DIR / "ofertas_ativas.json"
ENTIDADES_FILE = DATA_DIR / "entidades.json"
ESCOLAS_FILE = DATA_DIR / "escolas.json"
MAX_RECOMENDACOES = 3 # Number of closest entities to recommend

# --- Helper Functions ---
def load_json_data(file_path: pathlib.Path, default_value=None):
    if default_value is None:
        default_value = []
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_value

def save_json_data(data, file_path: pathlib.Path):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_school_location(cod_inep: str, escolas_data: list):
    for escola in escolas_data:
        if escola.get("codinep") == cod_inep:
            if "latitude" in escola and "longitude" in escola:
                return {"latitude": escola["latitude"], "longitude": escola["longitude"], "nome": escola.get("nome_escola", cod_inep)}
            elif "endereco" in escola: # Fallback to geocode address if lat/lon not present
                print(f"[INFO] Geocoding school {cod_inep} by address: {escola['endereco']}")
                coords = utils.geocode_address(escola["endereco"], escola.get("cep"))
                if coords:
                    return {"latitude": coords["latitude"], "longitude": coords["longitude"], "nome": escola.get("nome_escola", cod_inep)}
    print(f"[WARN] School location not found or could not be geocoded for INEP: {cod_inep}")
    return None

def parse_issue_body(issue_body_str: str) -> dict:
    """
    Parses the GitHub issue body (expected to be in a structured format,
    likely YAML-like from issue forms) into a dictionary.
    This is a simplified parser. A more robust one would use PyYAML or similar if the body is true YAML.
    Example line: - "escola_codinep: 11000001"
    """
    parsed_data = {}
    # A real implementation would use environment variables like GITHUB_TOKEN and GITHUB_REPOSITORY
    # and the github library to fetch issue details by number.
    # For this script, we assume the issue body is passed as a string or piped in.
    # This is a placeholder for robust issue parsing.
    # For now, let's assume the issue body format from `nova_oferta.yml` is simplified to key: value pairs
    # This needs to be adapted to how the actual issue body is formatted.
    # The example in README `create_oferta_from_issue.py "${{ github.event.issue.number }}"` implies
    # the script would use the GitHub API.

    # Placeholder: Assume issue_body_str is a simple string of key-value pairs for now.
    # This is a MAJOR simplification. In reality, you'd use the GitHub API.
    # For example, if issue_body_str was JSON string passed as arg:
    # try:
    #   return json.loads(issue_body_str)
    # except json.JSONDecodeError:
    #   print(f"[ERROR] Could not parse issue body as JSON: {issue_body_str}")
    #   return {}
    
    # For a simple key: value string like "escola_codinep:123
item:Arroz"
    for line in issue_body_str.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            parsed_data[key.strip()] = value.strip()
    return parsed_data


# --- Main Logic ---
def process_new_offer(issue_number: str, issue_title: str, issue_body: str, github_actor: str = "system"):
    """
    Processes a new food offer from a GitHub issue.
    Extracts details, finds nearby entities, and saves the offer.
    Returns information about the offer and recommended entities.
    """
    print(f"[INFO] Processing new offer from Issue #{issue_number}: {issue_title}")

    # This is where you'd use the GitHub API to get issue details if not passed directly
    # For now, we assume issue_body contains structured data.
    # This parsing needs to be robust based on actual issue form output.
    offer_details_from_issue = parse_issue_body(issue_body) # Simplified
    
    # Fallback to title for item if not in body (example of making it more robust)
    if not offer_details_from_issue.get("item") and "–" in issue_title:
        offer_details_from_issue["item"] = issue_title.split("–")[0].replace("[Oferta]", "").strip()
    if not offer_details_from_issue.get("escola_codinep") and "–" in issue_title: # Assuming school name/id in title
         title_parts = issue_title.split("–")
         if len(title_parts) > 1: # Heuristic
            potential_school_id = title_parts[1].strip()
            # This is a guess, actual school ID extraction needs to be solid
            if potential_school_id.isdigit(): # Check if it looks like an INEP code
                 offer_details_from_issue["escola_codinep"] = potential_school_id


    required_fields = ["escola_codinep", "item", "quantidade", "validade"]
    if not all(offer_details_from_issue.get(field) for field in required_fields):
        print(f"[ERROR] Missing required fields in issue #{issue_number}. Found: {offer_details_from_issue}")
        return None, []


    escolas_data = load_json_data(ESCOLAS_FILE)
    entidades_data = load_json_data(ENTIDADES_FILE)
    ofertas_ativas = load_json_data(OFERTAS_ATIVAS_FILE)

    school_inep = offer_details_from_issue.get("escola_codinep")
    school_location_info = get_school_location(school_inep, escolas_data)

    if not school_location_info:
        print(f"[WARN] Could not determine location for school INEP {school_inep}. Cannot perform geo-matching.")
        # Offer can still be saved, but without geo-recommendations
        # Or decide to fail if location is critical. For now, proceed.

    # Prepare new offer entry
    new_offer = {
        "id_issue": issue_number,
        "item": offer_details_from_issue.get("item"),
        "quantidade": offer_details_from_issue.get("quantidade"),
        "validade": offer_details_from_issue.get("validade"),
        "escola_codinep": school_inep,
        "escola_nome": school_location_info.get("nome") if school_location_info else school_inep,
        "observacoes": offer_details_from_issue.get("observacoes", ""),
        "data_publicacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "disponivel", # 'disponivel', 'reservada', 'coletada'
        "reservada_por_entidade_id": None,
        "coletada_por_entidade_id": None,
        "recomendacoes_geo": [] # To be filled
    }

    # Geo-matching logic
    recomendacoes = []
    if school_location_info:
        school_lat = school_location_info["latitude"]
        school_lon = school_location_info["longitude"]
        
        candidate_entities = []
        for entidade in entidades_data:
            if entidade.get("status") == "ativa" and "latitude" in entidade and "longitude" in entidade:
                dist = utils.calculate_distance(school_lat, school_lon,
                                                entidade["latitude"], entidade["longitude"])
                candidate_entities.append({
                    "nome": entidade["nome_entidade"],
                    "distancia_km": round(dist, 2),
                    "id_issue_entidade": entidade["id_issue"], # For contact or linking
                    "endereco": entidade.get("endereco_completo", "N/A")
                })
        
        # Sort by distance and take top N
        candidate_entities.sort(key=lambda x: x["distancia_km"])
        recomendacoes = candidate_entities[:MAX_RECOMENDACOES]
        new_offer["recomendacoes_geo"] = recomendacoes
        print(f"[INFO] Top {len(recomendacoes)} recommendations for offer #{issue_number}:")
        for rec in recomendacoes:
            print(f"  - {rec['nome']} ({rec['distancia_km']} km)")

    # Add to ofertas_ativas.json
    ofertas_ativas.append(new_offer)
    save_json_data(ofertas_ativas, OFERTAS_ATIVAS_FILE)
    print(f"[SUCCESS] Offer #{issue_number} processed and saved to {OFERTAS_ATIVAS_FILE}.")

    return new_offer, recomendacoes


if __name__ == "__main__":
    # This part simulates how the script might be called by a GitHub Action.
    # The GitHub Action would provide these values, e.g., from `github.event.issue`.
    # Usage: python scripts/create_oferta_from_issue.py <issue_number> <issue_title> <issue_body_json_string> <actor>
    # For simplicity, issue body parsing here is basic. A real script would use GitHub API.
    
    if len(sys.argv) > 3:
        issue_num_arg = sys.argv[1]
        issue_title_arg = sys.argv[2]
        # For issue_body, the GitHub Action might pass it as a JSON string,
        # or the script itself fetches it using the issue_num_arg and GitHub API.
        # The parse_issue_body function needs to be adapted accordingly.
        # Here, we'll assume a simplified key-value string for the body for CLI testing.
        issue_body_arg_str = sys.argv[3] # e.g. "escola_codinep:11000001
item:Arroz - 5kg
quantidade:10 pacotes
validade:31/12/2024"
        actor_arg = sys.argv[4] if len(sys.argv) > 4 else "cli_user"
        
        # Ensure data directory exists for local testing
        DATA_DIR.mkdir(exist_ok=True)
        # Create dummy files if they don't exist for local testing
        if not ENTIDADES_FILE.exists(): save_json_data([], ENTIDADES_FILE)
        if not ESCOLAS_FILE.exists(): save_json_data([], ESCOLAS_FILE)
        if not OFERTAS_ATIVAS_FILE.exists(): save_json_data([], OFERTAS_ATIVAS_FILE)

        print(f"Running script from CLI for issue {issue_num_arg}")
        new_offer_data, top_recs = process_new_offer(issue_num_arg, issue_title_arg, issue_body_arg_str, actor_arg)

        if new_offer_data:
            print("\n--- Resumo da Nova Oferta ---")
            print(json.dumps(new_offer_data, indent=2, ensure_ascii=False))
            if top_recs:
                print("\n--- Recomendações ---")
                for rec in top_recs:
                    print(f"- {rec['nome']} ({rec['distancia_km']} km) - Endereço: {rec['endereco']}")
            # In a GitHub Action, the 'top_recs' would be used to formulate a comment on the issue.
            # Example: comment_body = format_recommendation_comment(top_reacs)
            # then use GitHub API to post comment_body to issue_num_arg.
    else:
        print("Script for processing new food offers from GitHub Issues.")
        print("Usage: python create_oferta_from_issue.py <issue_number> <issue_title> <issue_body_string> [actor]")
        print("Example issue_body_string (for testing): "escola_codinep:11000001\nitem:Arroz Tipo 1\nquantidade:50 kg\nvalidade:31/12/2025"")
        print("\nTo test with sample data from _data folder (ensure escolas.json and entidades.json exist):")
        print("python scripts/create_oferta_from_issue.py 701 "[Oferta] Arroz Parboilizado – Escola Modelo 1" "escola_codinep:11000001\nitem:Arroz Parboilizado Tipo 1\nquantidade:50 kg\nvalidade:31/12/2024\nobservacoes:Pacotes de 5kg." test_user")
