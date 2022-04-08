FROM nikolaik/python-nodejs:latest
WORKDIR /foot
RUN mkdir /foot/app
RUN mkdir /foot/gameEngine
RUN mkdir /foot/logsGames
COPY /app/package.json /foot/app
RUN npm install --prefix /foot/app
COPY /app/dist /foot/app/dist
COPY /app/webapp /foot/app/webapp
COPY /app/*.js /foot/app/
COPY /app/*.db /foot/app/
COPY /gameEngine /foot/gameEngine
COPY /logsGames /foot/logsGames
COPY run_celery.sh /foot
RUN pip install -e /foot/gameEngine
# RUN pip install pyglet==y1.5.11
RUN pip install celery
# CMD ["node", "app/app.js"]
# CMD ["ls", "app"]