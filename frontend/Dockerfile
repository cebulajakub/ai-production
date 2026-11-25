
# ==========================================
# Stage 1: Build Angular application
# ==========================================

FROM node:24-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

RUN npm run build


# ==========================================
# Stage 2: Production runtime
# ==========================================

FROM nginx:alpine AS runtime

COPY --from=build /app/dist/frontend/browser/ /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
