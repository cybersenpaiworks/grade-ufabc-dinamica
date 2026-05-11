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
git clone https://github.com/cybersenpaiworks/grade-ufabc-dinamica.git
```

2. Suba a infraestrutura completa:
```bash
docker compose up -d --build
```

3. Acesse no navegador:
* Portal Web: `http://localhost:3000`
* Swagger (Documentação da API): `http://localhost:8000/docs`

## 💡 Destaques Técnicos

- Algoritmo customizado de Regex no backend para parsing de horários humanos e regras de negócio complexas (ex: turmas quinzenais pares/ímpares).
- Componentização orientada a dados no Svelte, com filtros multidimensionais simultâneos (Busca, Curso, Campus, Turno, Dia, Vagas).
- Validação automática de choque de horários na grade do aluno via UI.

---
**Desenvolvido por Gabriel Vancini.** Conheça mais soluções e projetos acessando [cybersenpaiworks.com.br](https://cybersenpaiworks.com.br).