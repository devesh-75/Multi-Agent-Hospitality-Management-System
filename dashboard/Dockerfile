FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 3000

# Custom nginx config to listen on 3000 and handle SPA routing
RUN sed -i 's/80/3000/g' /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
