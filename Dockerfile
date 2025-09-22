# ---- Base Stage ----
# Use a specific version of an official Node.js image based on Alpine Linux
FROM node:20-alpine AS base
WORKDIR /usr/src/app

# ---- Dependencies Stage ----
# Copy only package files and install dependencies to leverage Docker layer caching
FROM base AS dependencies
COPY package*.json ./
RUN npm install

# ---- Build Stage ----
# Copy source code and build the application
FROM dependencies AS build
COPY . .
# Replace 'npm run build' with your actual build command
RUN npm run build

# ---- Production Stage ----
# Create the final, lean production image
FROM base AS production
ENV NODE_ENV=production
# Copy only production dependencies from the 'dependencies' stage
COPY --from=dependencies /usr/src/app/node_modules ./node_modules
# Copy built application from the 'build' stage
COPY --from=build /usr/src/app/dist ./dist

# Expose the application port
EXPOSE 3000

# Command to run the application
CMD ["node", "dist/main.js"]