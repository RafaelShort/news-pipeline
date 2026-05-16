# 📰 News Pipeline

Pipeline automatizado de coleta, processamento e busca de artigos de notícias,
com IA (NER, classificação de tópicos e sumarização).

---

## Funcionalidades

- **Coleta automática** de feeds RSS em intervalo configurável
- **Fila de mensagens** com Apache Kafka
- **Enriquecimento com IA:**
  - Reconhecimento de entidades (NER)
  - Classificação de tópicos
  - Sumarização automática de artigos
- **Busca full-text** com Elasticsearch
- **Filtros por facetas** (fonte, tópico, idioma, data)
- **Interface web** moderna com React e Tailwind CSS

---

## Tecnologias

### Backend
| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| Apache Kafka | Fila de mensagens entre producer e workers |
| Elasticsearch | Indexação e busca de artigos |
| HuggingFace Transformers | Modelos de NLP (NER, classificação, sumarização) |
| GraphQL | API de consulta para o frontend |

### Frontend
| Tecnologia | Uso |
|---|---|
| React | Interface do usuário |
| Tailwind CSS | Estilização |
| Vite | Build e dev server |
| date-fns | Formatação de datas |
| lucide-react | Ícones |

### Infraestrutura
| Tecnologia | Uso |
|---|---|
| Docker | Orquestração dos serviços |

---

## Como rodar localmente

### Pré-requisitos

- [Docker](https://www.docker.com/) instalado
- [Node.js](https://nodejs.org/) 18+
- Python 3.10+

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/news-pipeline.git
cd news-pipeline
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

### 3. Suba a infraestrutura

```bash
docker compose up -d
```

### 4. Instale as dependências Python

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate

pip install -r requirements.txt
```

### 5. Instale as dependências do frontend

```bash
cd frontend
npm install
npm run dev
```
