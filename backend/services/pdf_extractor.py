import pdfplumber
import pandas as pd
import re
import json

def extrair_horarios(horario_str):
    """
    Transforma strings complexas e múltiplas em um array de objetos estruturados:
    'terça das 10:00 às 12:00, quinzenal I; sexta das 08:00 às 10:00, semanal'
    """
    if pd.isna(horario_str) or not isinstance(horario_str, str):
        return []
        
    # Quebra a string caso haja blocos separados por ponto e vírgula
    blocos = str(horario_str).split(';')
    resultados = []
    
    # O regex agora é insensível a maiúsculas/minúsculas (re.IGNORECASE)
    # [aáà]s previne que erros de crase no PDF quebrem o código
    # O final do regex captura opcionalmente a frequência ("semanal", "quinzenal I", "quinzenal II")
    padrao = re.compile(
        r'(?P<dia>[a-zçáéíóú]+)\s+das\s+(?P<inicio>\d{2}:\d{2})\s+[aáà]s\s+(?P<fim>\d{2}:\d{2})(?:,\s*(?P<frequencia>[a-z\s]+i{0,2}))?', 
        re.IGNORECASE
    )
    
    for bloco in blocos:
        encontros = re.finditer(padrao, bloco.strip())
        for match in encontros:
            freq_bruta = match.group('frequencia')
            # Limpa espaços e padroniza tudo para minúsculo, assumindo 'semanal' se omitido no PDF
            freq_normalizada = freq_bruta.strip().lower() if freq_bruta else 'semanal'
            
            resultados.append({
                "dia": match.group('dia').lower(),
                "inicio": match.group('inicio'),
                "fim": match.group('fim'),
                "frequencia": freq_normalizada
            })
            
    return resultados

def extrair_tabela_pdf(caminho_arquivo: str) -> list:
    todas_linhas = []
    
    with pdfplumber.open(caminho_arquivo) as pdf:
        for pagina in pdf.pages:
            tabela = pagina.extract_table()
            if tabela:
                todas_linhas.extend(tabela)
                
    if not todas_linhas:
        return []
        
    cabecalhos = todas_linhas[0]
    dados = todas_linhas[1:]
    
    df = pd.DataFrame(dados, columns=cabecalhos)
    
    # 1. Limpeza Base
    df = df.replace(r'\n', ' ', regex=True)
    df.columns = [str(col).replace('\n', ' ').strip().upper() for col in df.columns]
    df = df.dropna(how='all')
    
    # [NOVO] Remove as repetições de cabeçalho geradas pelas quebras de página do PDF.
    # Verifica dinamicamente qual é a primeira coluna (ex: 'CURSO') e remove as linhas 
    # onde o valor da célula for a palavra 'CURSO'.
    nome_primeira_coluna = df.columns[0]
    df = df[df[nome_primeira_coluna] != nome_primeira_coluna]
    
    # 2. Estruturação de Data/Hora (Magia do Pandas)
    if 'TEORIA' in df.columns:
        df['HORARIOS_TEORIA'] = df['TEORIA'].apply(extrair_horarios)
    if 'PRÁTICA' in df.columns:
        df['HORARIOS_PRATICA'] = df['PRÁTICA'].apply(extrair_horarios)
        
    # Removemos as colunas de texto antigas para economizar banda na API
    colunas_para_remover = [col for col in ['TEORIA', 'PRÁTICA'] if col in df.columns]
    df = df.drop(columns=colunas_para_remover)
    
    # 3. Converte para uma lista de dicionários (pronto para virar JSON na API)
    return df.to_dict(orient='records')

if __name__ == "__main__":
    arquivo = "../ajuste_matriculas_2026_2_turmas.pdf" 
    dados_processados = extrair_tabela_pdf(arquivo)
    
    if dados_processados:
        print("Sucesso! Veja como o primeiro registro ficou estruturado para a API:\n")
        # Mostra o primeiro registro formatado como JSON
        print(json.dumps(dados_processados[0], indent=2, ensure_ascii=False))
    else:
        print("Nenhum dado encontrado.")