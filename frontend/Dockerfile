version: '3.8'

services:
  redis:
    image: redis:alpine
    container_name: pdf_redis
    restart: unless-stopped
    command: redis-server --save 60 1 --loglevel warning
    volumes:
      # Persistência de dados seguindo o seu padrão de organização
      - /home/cybersenpai/docker-data/extrator-pdf/redis:/data
    networks:
      - proxy-network

  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    container_name: pdf_backend
    restart: unless-stopped
    expose:
      - "8000" # Acessível apenas dentro da proxy-network
    depends_on:
      - redis
    networks:
      - proxy-network

  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile
    container_name: pdf_frontend
    restart: unless-stopped
    expose:
      - "3000" # O NPM ou Cloudflare Tunnel vai apontar para cá
    depends_on:
      - backend
    labels:
      # Labels integradas ao seu Dashboard/Hub
      hub.enable: "true"
      hub.name: "Grade UFABC"
      hub.host: "grade.cybersenpaiworks.com.br"
      hub.scheme: "https"
      hub.icon: "📅"
      hub.description: "Portal dinâmico para extração e montagem de grade de disciplinas."
    networks:
      - proxy-network

networks:
  proxy-network:
    external: true