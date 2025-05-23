import json, xml.etree.ElementTree as ET, pathlib, requests, tempfile

SIGPC_URL = "https://s3.amazonaws.com/sigpc-data/ultimos_90_dias.xml"

def baixar_xml(url: str) -> pathlib.Path:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xml")
    tmp.write(requests.get(url, timeout=60).content)
    tmp.close()
    return pathlib.Path(tmp.name)

def extrair(xml_path: pathlib.Path) -> list[dict]:
    root = ET.parse(xml_path).getroot()
    ofertas = []
    for comp in root.findall(".//compra"):
        item = comp.findtext("descricao")
        data = comp.findtext("data_compra")
        qtd  = float(comp.findtext("quantidade"))
        if qtd == 0:
            continue
        ofertas.append({"item": item, "data_compra": data, "quantidade": qtd})
    return ofertas

def main():
    xml = baixar_xml(SIGPC_URL)
    dados = extrair(xml)
    pathlib.Path("_data").mkdir(exist_ok=True)
    with open("_data/potencial_vencimento.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
