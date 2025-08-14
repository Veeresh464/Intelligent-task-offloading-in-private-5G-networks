FROM node:16-alpine

WORKDIR /app


RUN npm init -y
RUN npm install express
RUN npm install multer


COPY index.js .

EXPOSE 8080

CMD ["node", "index.js"]
