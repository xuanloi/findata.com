FROM node:14-alpine
WORKDIR /src
COPY . /src
RUN rm -rf node_modules
RUN npm install
RUN npm run build

ENV HOST 0.0.0.0
#CMD ["npm", "run", "start"]