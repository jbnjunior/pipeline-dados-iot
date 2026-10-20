# Pipeline de Dados com IoT e Docker

Projeto acadêmico de ingestão, armazenamento e visualização de leituras de temperatura de dispositivos IoT usando Python, PostgreSQL em Docker, SQLAlchemy, Streamlit e Plotly.

## Arquitetura

1. **Fonte:** CSV do dataset [Temperature Readings: IoT Devices no Kaggle](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices).
2. **Processamento:** `src/ingest.py` lê o CSV, padroniza colunas, converte data/temperatura, remove registros inválidos e duplicados.
3. **Armazenamento:** PostgreSQL executado em contêiner Docker.
4. **Análise:** quatro views SQL agregam dados por dispositivo, hora e dia.
5. **Visualização:** `dashboard.py` mostra métricas e gráficos interativos.

## Estrutura

```text
pipeline-dados-iot/
├── dashboard.py
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
├── src/
│   ├── __init__.py
│   ├── db.py
│   └── ingest.py
├── sql/
│   └── views.sql
├── data/
│   └── temperature-readings-iot-devices.csv  # baixar do Kaggle; não versionar
├── screenshots/                               # salvar capturas do dashboard
└── docs/
    └── relatorio_modelo.pdf
```

## Pré-requisitos

- Python 3.10 ou superior
- Docker Desktop instalado e em execução
- Git e conta no GitHub
- CSV baixado do Kaggle

## Configuração no Windows (PowerShell)

Abra o terminal na pasta do projeto.

### 1. Criar ambiente virtual e instalar dependências

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Se o PowerShell bloquear a ativação, use o terminal CMD e execute:
```bat
.venv\Scripts\activate.bat
```

### 2. Configurar variáveis de ambiente

Copie `.env.example` para `.env` e altere `POSTGRES_PASSWORD` para uma senha sua. O `.env` não deve ser enviado ao GitHub.

PowerShell:
```powershell
Copy-Item .env.example .env
```

### 3. Baixar o CSV

Entre no Kaggle, baixe o arquivo CSV do dataset e coloque-o na pasta `data/` com o nome exato:

`temperature-readings-iot-devices.csv`

Confira se o arquivo não ficou dentro de uma segunda pasta após descompactar.

### 4. Iniciar o PostgreSQL no Docker

```powershell
docker compose up -d
docker compose ps
```

Espere o serviço ficar saudável antes de continuar. Para ver os logs:
```powershell
docker compose logs -f postgres
```

### 5. Processar e inserir os dados

Na raiz do projeto, com o ambiente virtual ativo:
```powershell
python -m src.ingest
```

O script informa quantas linhas válidas foram lidas e quantas leituras existem no banco. Ele evita inserir duplicatas se for executado novamente.

Se o CSV tiver outro nome ou caminho:
```powershell
python -m src.ingest --csv "C:\caminho\para\arquivo.csv"
```

### 6. Criar as views SQL

```powershell
Get-Content .\sql\views.sql | docker exec -i postgres-iot psql -U iot_user -d iot_db
```

Confirme que existem:
```powershell
docker exec -it postgres-iot psql -U iot_user -d iot_db -c "\dv"
docker exec -it postgres-iot psql -U iot_user -d iot_db -c "SELECT COUNT(*) FROM temperature_readings;"
```

### 7. Abrir o dashboard

```powershell
streamlit run dashboard.py
```

O terminal exibirá o endereço local, normalmente `http://localhost:8501`. Abra-o no navegador. Para atualizar os dados após nova ingestão, recarregue a página.

## Views SQL e propósito

1. **`avg_temp_por_dispositivo`**: calcula média, mínimo, máximo e número de leituras por dispositivo. Ajuda a comparar sensores e identificar valores atípicos.
2. **`leituras_por_hora`**: conta as leituras por hora do dia. Ajuda a verificar em quais horários há maior volume de registros e possíveis lacunas de coleta.
3. **`temp_max_min_por_dia`**: apresenta temperaturas máxima, mínima, média e total de leituras por dia. Ajuda a observar variações e tendências diárias.
4. **`resumo_dataset`** (apoio): resume o volume, o número de dispositivos e o intervalo temporal dos dados.

## Capturas de tela

Depois de executar o dashboard, tire capturas reais dos três gráficos e salve em `screenshots/`. Insira as imagens aqui antes de entregar, por exemplo:

- `screenshots/dashboard-geral.png`
- `screenshots/media-dispositivos.png`
- `screenshots/temperaturas-diarias.png`

Não inclua imagens fictícias como se fossem resultados executados.

## Possíveis insights para investigar

- Qual dispositivo tem maior e menor temperatura média?
- Em quais horas há mais leituras? Existem horas sem registros?
- Em quais dias ocorreu a maior amplitude entre máxima e mínima?
- Há dispositivos com poucas leituras em comparação com os demais?

Preencha as conclusões do relatório **depois de observar os gráficos reais**. Não assuma valores antes de processar o dataset.

## Comandos Git e GitHub

Crie um repositório público vazio no GitHub (não adicione README pelo site, pois já existe localmente). Na raiz do projeto:

```bash
git init
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
git add .
git commit -m "Projeto inicial: Pipeline de Dados IoT"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/pipeline-dados-iot.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu usuário e use a URL real do repositório. Para atualizar depois:
```bash
git add .
git commit -m "Atualiza pipeline e documentação"
git push
```

Para baixar mudanças feitas no GitHub:
```bash
git pull
```

## Encerrar ou reiniciar

```powershell
docker compose stop       # para o banco sem apagar os dados
docker compose start      # inicia novamente
docker compose down       # remove o contêiner, preserva o volume
docker compose down -v    # APAGA também os dados do banco; use com cuidado
```

## Limitações

O dataset é histórico e estático, não uma transmissão IoT em tempo real. O projeto demonstra o fluxo de dados inspirado em IoT; em produção, sensores enviariam eventos continuamente por MQTT ou HTTP e seria necessário acrescentar monitoramento, autenticação, tratamento de falhas e política de retenção.
