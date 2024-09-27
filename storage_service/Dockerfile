FROM node:14

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Asegurar permisos adecuados para el directorio de la base de datos
RUN mkdir -p /app && chmod -R 777 /app

EXPOSE 5003

CMD ["node", "app.js"]
