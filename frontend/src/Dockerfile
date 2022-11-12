FROM node:16
WORKDIR /home/app/tasks/frontend
COPY package*.json ./
RUN curl -v https://registry.npmjs.com/
RUN npm install
COPY ./ ./
RUN npm run build
RUN npm install -g serve