# Django Budget project

## Requirements
- Docker
- Docker Compose

## Development
- Clone project
- Save `.env.example` as `.env` and add/edit settings in this file;
- Run `make build`, only for install or update project's dependencies;
- Run `make start` for start project in detach mode;
- Run `make start_` for start project;
- Run `make manage c=migrate` for appling DB migrations (in other console window);
- Run `make manage c=createsuperuser` for creating an admin user for access to admin area ;
- Visit `localhost:8000`;
- To shut down project run `make stop`;
- If you can't use make see `makefile` for correct docker command;