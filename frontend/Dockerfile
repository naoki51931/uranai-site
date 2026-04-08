FROM node:20-alpine

WORKDIR /app

ARG NEXT_PUBLIC_SITE_URL=http://localhost
ARG INTERNAL_API_BASE_URL=http://backend:8000
ENV NEXT_PUBLIC_SITE_URL=${NEXT_PUBLIC_SITE_URL}
ENV INTERNAL_API_BASE_URL=${INTERNAL_API_BASE_URL}

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

RUN npm run build

CMD ["npm", "run", "start"]
