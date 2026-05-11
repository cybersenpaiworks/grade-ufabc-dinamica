# frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Copia os arquivos de dependência e instala
COPY package*.json ./
RUN npm ci

# Copia o resto do código e compila a aplicação para produção
COPY . .
RUN npm run build

# --- Estágio Final ---
FROM node:20-alpine

WORKDIR /app

# Copia apenas os arquivos necessários da etapa de build
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# A porta padrão do adapter-node é a 3000
EXPOSE 3000

# Inicia o servidor Node otimizado
CMD ["node", "build/index.js"]