# 📅 Extrator Dinâmico de Grade (UFABC)

Um portal web dinâmico projetado para processar, higienizar e visualizar grades de horários complexas a partir de arquivos PDF desestruturados. 

Este projeto resolve o problema crônico de visualização de horários acadêmicos cruzando informações de turmas, frequência quinzenal e vagas livres em uma interface de altíssima performance.

## 🚀 Tecnologias Utilizadas

A arquitetura foi desenhada seguindo o padrão de **Monorepo**, dividindo responsabilidades entre extração pesada de dados e renderização reativa no cliente.

* **Frontend:** SvelteKit (TypeScript) adaptado para Node.js. (Alta performance na renderização de milhares de linhas sem Virtual DOM).
* **Backend:** FastAPI (Python) responsável pela sanitização via `pandas` e leitura visual de tabelas via `pdfplumber`.
* **Banco de Dados/Sessão:** Redis para armazenamento em memória ultra-rápido.
* **Infraestrutura:** Docker e Docker Compose com rede de proxy isolada.

## ⚙️ Como executar o projeto localmente

Pré-requisitos: Docker e Docker Compose instalados.

1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/extrator-pdf-dinamico.git](https://github.com/SEU_USUARIO/extrator-pdf-dinamico.git)