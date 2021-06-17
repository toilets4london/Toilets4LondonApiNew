# Work In Progress / Experimental - Toilets4London Api V2

- This reimplementation is supposed to make this API more scalable to other cities, as data can be loading incrementally, based on location.
- A new Toilet schema is being trialled with new fields, based on expert recommendation and user research. This would cover more details such as RADAR key, changing places etc.
- This piece of work will also involve improvement of the web scraping scripts, in order to attempt to extract more detailed info wherever possible.

### Use of Docker

#### Running in development (locally)

This workflow has been tested using WSL2 on Windows (with Docker installed).

```console
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up
```

- May have to run `docker-compose -f docker-compose.yml down` and then `docker-compose -f docker-compose.yml up` if an error comes up with the docker-compose command trying to run migrations before database is ready.
- Making changes to the api code (located in `ToiletApiNew/`) and saving will reload django 

To make migrations

```console
docker-compose -f docker-compose.yml exec web python3 manage.py makemigrations
```

To create superuser

```console
docker-compose -f docker-compose.yml exec web python3 manage.py createsuperuser
```

To bring down containers and volumes 

```console
docker-compose -f docker-compose.yml down -v
```

#### Staging 

- Run staging containers on a remote server (has been tested on Ubuntu 20.04 on Digital Ocean)
- First install docker and docker compose (https://docs.docker.com/engine/install/ubuntu/)
- Copy over all the repo code (eg via git pull) to the remote server
- Create the required files (`.env.staging`, `.env.staging.db`, `.env.staging.proxy-companion`) on the remote server (see notes about the contents of these files below)

```console
docker-compose -f docker-compose.staging.yml up -d --build
docker-compose -f docker-compose.staging.yml exec web python3 manage.py migrate --noinput
docker-compose -f docker-compose.staging.yml exec web python3 manage.py collectstatic --no-input --clear
```

To create superuser (only run once)

```console
docker-compose -f docker-compose.staging.yml exec web python3 manage.py createsuperuser
```

#### Production (remote)

Bring down staging containers if needed

```console
docker-compose -f docker-compose.staging.yml down -v
```

Very similar to staging - run

```console
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python3 manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python3 manage.py collectstatic --no-input --clear
```

To create superuser (only run once)

```console
docker-compose -f docker-compose.prod.yml exec web python3 manage.py createsuperuser
```


#### Contents of .env.staging or .env.prod
DEBUG=0
SECRET_KEY=longrandomstring
DJANGO_ALLOWED_HOSTS=<yourdomain>
SQL_ENGINE=django.contrib.gis.db.backends.postgis
SQL_DATABASE=<databasename>
SQL_USER=<databaseuser>
SQL_PASSWORD=<databasepassword>
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
VIRTUAL_HOST=<yourdomain>
VIRTUAL_PORT=8000
LETSENCRYPT_HOST=<yourdomain>

#### Contents of .env.staging.proxy-companion or .env.prod.proxy-companion
DEFAULT_EMAIL=<youremail>
ACME_CA_URI=https://acme-staging-v02.api.letsencrypt.org/directory *only use this in staging*
NGINX_PROXY_CONTAINER=nginx-proxy

#### Contents of .env.staging.db or .env.prod.db
POSTGRES_USER=<databaseuser>
POSTGRES_PASSWORD=<databasepassword>
POSTGRES_DB=<databasename>