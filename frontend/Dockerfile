FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

RUN addgroup --system astra && adduser --system --group astra && chown -R astra:astra /app
USER astra

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
