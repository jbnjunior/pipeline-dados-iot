# Pipeline de Dados com IoT e Docker

## Sobre o projeto

Este projeto implementa um pipeline de dados para processar leituras históricas de temperatura de dispositivos IoT, armazená-las em um banco de dados PostgreSQL e disponibilizar análises por meio de um dashboard interativo.

O objetivo é demonstrar o uso de ferramentas de engenharia de dados para ingestão, armazenamento, consulta e visualização de informações.

## Tecnologias utilizadas

- Python
- Docker e Docker Compose
- PostgreSQL
- Pandas
- Streamlit
- Plotly
- SQL

## Estrutura do projeto

- `src/`: conexão com o banco de dados e ingestão dos dados.
- `sql/views.sql`: criação das views para análise.
- `dashboard.py`: dashboard interativo.
- `docker-compose.yml`: configuração do PostgreSQL.
- `requirements.txt`: dependências Python.
- `docs/`: relatórios do projeto.
- `screenshots/`: capturas de tela do projeto.
- `gerar_relatorio.py`: script de geração do relatório em PDF.

## Como executar

### 1. Preparar o ambiente

Instale Python e Docker Desktop. Clone este repositório e entre na pasta do projeto.

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 2. Iniciar o PostgreSQL

```bash
docker compose up -d
```

### 3. Importar os dados

Coloque o arquivo CSV do dataset na pasta `data/` e execute:

```bash
python -m src.ingest --csv data/IOT-temp.csv
```

### 4. Criar as views SQL

```bash
docker exec -i postgres-iot psql -U iot_user -d iot_db < sql/views.sql
```

### 5. Abrir o dashboard

```bash
streamlit run dashboard.py
```

O dashboard estará disponível no endereço local informado pelo Streamlit, normalmente `http://localhost:8501`.

## Dataset

O projeto utiliza o dataset Temperature Readings of IoT Devices, disponível no Kaggle:

https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices

Os dados analisados são históricos e não representam uma transmissão de leituras em tempo real.

## Relatório

O relatório do projeto está disponível em `docs/relatorio_final.pdf`.

## Autor

**Juarez Barra Nova Junior**

Curso: Análise e Desenvolvimento de Sistemas

Disciplina: Disruptive Architectures: IoT, Big Data e IA
