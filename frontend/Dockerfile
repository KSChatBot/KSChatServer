# Pull latest official node image
FROM node:latest

# Set working directory
WORKDIR /app

# Add /app/node_modules/.bin to environment variables
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies 
COPY ./package*.json ./

RUN npm install

COPY . .

# Add React app to working directory
ADD . /app

EXPOSE 8080

# Start the React app
CMD ["npm", "start"]