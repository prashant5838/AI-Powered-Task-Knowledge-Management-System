FROM node:18
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . /app
ENV CHOKIDAR_USEPOLLING=true
CMD ["npm", "start"]
