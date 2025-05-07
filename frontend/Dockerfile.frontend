# Estágio de build
FROM node:20-alpine AS build

WORKDIR /app

# Copiar arquivos de configuração primeiro para aproveitar o cache
COPY package.json .
COPY package-lock.json* .
COPY bun.lockb* .

# Instalar dependências
RUN npm ci

# Copiar o restante do código
COPY . .

# Construir a aplicação
RUN npm run build

# Estágio de produção
FROM nginx:alpine AS production

# Copiar arquivos de build para o diretório do nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuração personalizada do nginx (opcional)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor a porta 80
EXPOSE 80

# Comando para iniciar o nginx
CMD ["nginx", "-g", "daemon off;"]