Abaixo segue um “pacote de arranque” para o Heta (**Humanizando Excedentes Trocando Alimentos**) já aderente ao seu desenho backendless.
Incluí esboços de arquivos-chave, dicas de segurança/confiabilidade e próximos passos para que você possa literalmente clonar, “pushar” e testar com uma escola piloto ainda hoje.

---

## 1 · Estrutura de repositório pronta-para-usar

```
Heta/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── nova_oferta.yml
│   │   └── cadastro_entidade.yml
│   └── workflows/
│       ├── ingest_sigpc.yml
│       ├── process_oferta.yml
│       ├── process_coleta.yml
│       └── deploy_pwa.yml
├── pwa/               # SvelteKit ou Vue – vazio agora
├── scripts/
│   ├── parse_sigpc.py
│   ├── create_oferta_from_issue.py
│   └── update_oferta_status.py
├── _data/             # commitado vazio (gitkeep) – Actions preenchem
└── README.md
```

---

## 2 · ISSUE TEMPLATES (`.github/ISSUE_TEMPLATE/…`)

### `nova_oferta.yml`

```yaml
name: "🍎 Nova Oferta de Excedente"
description: Use este formulário para registrar alimento excedente.
title: "[Oferta] {{ item }} – {{ escola }}"
labels: [oferta-disponivel]
body:
  - type: input
    id: escola_codinep
    attributes:
      label: Código INEP da escola
      placeholder: "e.g. 11000001"
    validations: { required: true }
  - type: input
    id: item
    attributes: { label: Produto, placeholder: "Arroz tipo 1 – 5 kg" }
    validations: { required: true }
  - type: input
    id: quantidade
    attributes: { label: Quantidade, placeholder: "12 kg" }
    validations: { required: true }
  - type: input
    id: validade
    attributes: { label: Data de validade (DD/MM/AAAA) }
    validations: { required: true }
  - type: textarea
    id: observacoes
    attributes: { label: Observações adicionais, placeholder: "Lote lacrado, armazenado em local seco." }
```

### `cadastro_entidade.yml` (resumido)

```yaml
name: "✅ Cadastro de Entidade Receptora"
title: "[Entidade] {{ nome }}"
labels: [entidade-pendente]
body:
  - type: input
    id: cnpj
    attributes: { label: CNPJ }
    validations: { required: true }
  - type: input
    id: email
    attributes: { label: E-mail para contato }
    validations: { required: true }
  - type: input
    id: telefone
    attributes: { label: Telefone/WhatsApp }
  - type: textarea
    id: descricao
    attributes: { label: Descrição curta da entidade }
```

---

## 3 · WORKFLOWS

### `ingest_sigpc.yml` — baixa XMLs e gera “potencial vencimento”

```yaml
name: Ingestão SIGPC
on:
  schedule:
    - cron: '0 3 * * *'  # 03:00 UTC ≅ 00:00 BRT
jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install deps
        run: python -m pip install -r scripts/requirements.txt
      - name: Run parser
        run: python scripts/parse_sigpc.py
      - name: Commit & push
        uses: EndBug/add-and-commit@v9
        with:
          add: '_data/potencial_vencimento.json'
          message: 'chore(data): atualiza potencial_vencimento.json'
```

### `process_oferta.yml` — converte Issue → `_data/ofertas_ativas.json`

```yaml
name: Processa Nova Oferta
on:
  issues:
    types: [opened]
jobs:
  oferta:
    if: github.event.issue.labels.* contains 'oferta-disponivel'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: python -m pip install -r scripts/requirements.txt
      - run: python scripts/create_oferta_from_issue.py "${{ github.event.issue.number }}"
      - uses: EndBug/add-and-commit@v9
        with:
          add: '_data/ofertas_ativas.json'
          message: 'feat(oferta): adiciona oferta #${{ github.event.issue.number }}'
```

### `process_coleta.yml` — trata comentários de interesse

```yaml
name: Reserva/Coleta
on:
  issue_comment:
    types: [created]
jobs:
  coleta:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: python -m pip install -r scripts/requirements.txt
      - run: python scripts/update_oferta_status.py "${{ github.event.comment.body }}" "${{ github.event.issue.number }}"
      - uses: EndBug/add-and-commit@v9
        with:
          add: '_data/ofertas_ativas.json _data/historico_doacoes.csv'
          message: 'chore(oferta): atualiza status oferta'
```

### `deploy_pwa.yml` — build & publish no GitHub Pages

```yaml
name: Deploy PWA
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: |
          cd pwa
          npm ci
          npm run build   # configure conforme framework
      - name: Publish
        uses: peaceiris/actions-gh-pages@v4
        with:
          publish_dir: ./pwa/dist   # ajuste p/ pasta final
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

---

## 4 · SCRIPTS (Python)

### Exemplo: `parse_sigpc.py` (trecho-chave)

```python
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
```

*(os outros scripts só precisam ler/escrever `_data/ofertas_ativas.json` e usar `git python`-friendly APIs como `ruamel.yaml` ou `json` + commit).*

---

## 5 · Git-race conditions & locking simples

```yaml
# Em todos os jobs que escrevem no mesmo arquivo:
concurrency:
  group: ${{ github.workflow }}
  cancel-in-progress: false
```

Isso coloca os jobs em fila (máximo uma escrita por vez) e evita conflitos de merge.

---

## 6 · Segurança & privacidade no MVP

| Risco                                                  | Mitigação mínima                                                                                                                                  |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dados pessoais em JSON público                         | Use apenas **código INEP** e apelido da entidade; contatos trocados via e-mail fora da Issue.                                                     |
| Spam/abuso de Issues                                   | Restrinja “Issues” a usuários convidados (Settings → Collaborators) ou repositório privado.                                                       |
| Token PAT no frontend (caso adote `workflow_dispatch`) | **Evitar** no MVP; se necessário, gere token “fine-grained” com escopo *single repository* e injete via `Netlify Edge Function` em backend-proxy. |

---

## 7 · Roadmap imediato (7 dias)

| Dia | Entrega                                                                          | Ferramenta            |
| --: | -------------------------------------------------------------------------------- | --------------------- |
|   1 | Repo criado + workflows vazios                                                   | GitHub                |
|   2 | Templates de Issue prontos                                                       | GitHub UI             |
|   3 | Script `parse_sigpc.py` funcional                                                | Python                |
|   4 | Script `create_oferta_from_issue.py` + JSON schema (`_data/ofertas_ativas.json`) | Python + `jsonschema` |
|   5 | PWA stub: lista ofertas via `fetch()`                                            | SvelteKit/Vue         |
|   6 | Processo completo “Oferta → Reserva” validado com **1 escola** fake              | Issues                |
|   7 | Retrospectiva + checklist de gaps (UX, labels, docs)                             | README                |

---

## 8 · Próximos saltos pós-MVP

1. **Autenticação GitHub OAuth** no PWA para abrir/commentar Issues sem sair da interface.
2. **Geo-matching automático** no `update_oferta_status.py` — recomendar entidade mais próxima e mencionar no comentário.
3. **Dashboards em Vega-Lite** renderizando `_data/historico_doacoes.csv` direto no PWA.
4. Exportar histórico em formato **Open Refine/CKAN** para transparência externa.

---

### TL;DR

*Você já tem um “lego set” completo:* basta colar esses arquivos no repo, ajustar URLs e rodar. Em poucas horas será possível demonstrar o fluxo ponta-a-ponta usando somente recursos grátis do GitHub. Isso valida participação dos usuários e a robustez dos dados **antes** de investir em banco, fila ou container.
