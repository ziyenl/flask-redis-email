# Running the flask app

---
After git clone, run the following commands:
- `flask run`: runs the flask app
- `flask db init`: interacts with alembic to create the migrations folder)
- `flask  db migrate`: compare existing database model and create the script to go from one revision to the other
- `flask db upgrade`: applies the changes to the database

---
To use docker, you can build the docker image
- `docker build -t <IMAGE_NAME> .`: builds the docker image
- `docker run -dp 5007:5000 -w /app -v "$(pwd):/app" <IMAGE_NAME> sh -c "flask run"`: creates the docker container and run it using flask
If you need to use a different db, set the setting through .env

---
Specify mail gun and redis URL configuration in the .env file
`MAILGUN_API_KEY=<insert api key here>`
`MAILGUN_DOMAIN=<insert your domain here>`
`REDIS_URL=<insert redis url>`

---
Run the flask app and background worker separately ensuring both has the same code base if you are running it locally
- Flask App
`docker run -p 5000:5000 <DOCKER_IMAGE_NAME> sh -c "flask run --host 0.0.0.0"`
- Background Worker
`docker run -w /app <DOCKER_IMAGE_NAME> sh -c "rq worker -u <REDIS_EXTERNAL_URL> <QUEUE_NAME>"`

---
For deployment to production,add a docker command to configure the settings of the background worker
`/bin/bash -c cd /app && rq worker -c settings`