# Build stage
FROM node:18-alpine as build
WORKDIR /app

# Copy shared module first to cache dependencies
COPY ai-resume-shared ./ai-resume-shared

# Copy web module
COPY ai-resume-web ./ai-resume-web

# Install dependencies and build
WORKDIR /app/ai-resume-web
RUN npm install
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/ai-resume-web/dist /usr/share/nginx/html
COPY ai-resume-web/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
