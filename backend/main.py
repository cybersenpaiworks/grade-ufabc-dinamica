from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

# Importando o motor que acabamos de criar
from services.pdf_extractor import extrair_tabela_pdf

app = FastAPI(
    title="Extrator de Turmas Dinâmico",
    description="API para conversão de PDFs de turmas em dados estruturados",
    version="1.0"
)

# Configuração de CORS: Essencial para permitir que o frontend no SvelteKit
# faça requisições para esta API sem ser bloqueado pelo navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em ambiente de produção, amarraremos isso ao seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/extrair-turmas")
async def extrair_turmas(arquivo: UploadFile = File(...)):
    """
    Recebe um PDF via form-data, processa as tabelas e horários, 
    e devolve um JSON estruturado pronto para consumo dinâmico.
    """
    if not arquivo.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="O arquivo enviado precisa ser um PDF.")
        
    caminho_temp = f"temp_{arquivo.filename}"
    
    try:
        # Salva o arquivo temporariamente no servidor para o pdfplumber conseguir ler
        with open(caminho_temp, "wb") as buffer:
            shutil.copyfileobj(arquivo.file, buffer)
            
        # Aciona a nossa lógica de domínio isolada
        dados = extrair_tabela_pdf(caminho_temp)
        
        return {
            "status": "sucesso", 
            "total_registros": len(dados), 
            "dados": dados
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar o PDF: {str(e)}")
        
    finally:
        # Boas práticas: sempre limpar o lixo temporário do container/servidor
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)