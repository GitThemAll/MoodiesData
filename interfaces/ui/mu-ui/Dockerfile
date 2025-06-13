FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy rest of the source
COPY . .

# Build the app
RUN npm run build

EXPOSE 3000

VOLUME ["/app/resources"]

CMD ["npm", "start"]