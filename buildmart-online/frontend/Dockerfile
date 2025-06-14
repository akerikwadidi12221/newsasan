FROM node:18 AS build
WORKDIR /app
COPY package.json tsconfig.json vite.config.ts ./
COPY public ./public
COPY src ./src
RUN npm install && npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY ../nginx/nginx.conf /etc/nginx/nginx.conf
CMD ["nginx", "-g", "daemon off;"]
