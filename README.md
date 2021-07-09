# ITR Portflio Alignment Tool

Under the hood, this API uses the ITR Python module. The complete structure that consists of a Python module, API and a UI looks as follows:

    +-------------------------------------------------+
    |   UI     : To be build                          |
    |                                                 |
    | +-----------------------------------------+     |
    | | REST API: Dockerized FastAPI/NGINX      |     |
    | | Source : github.com/os-c/ITR_api        |     |
    | | Install: via source or dockerhub        |     |
    | |                                         |     |
    | | +---------------------------------+     |     |
    | | |                                 |     |     |
    | | |Core   : Python Module           |     |     |
    | | |Source : github.com/os-c/ITR     |     |     |
    | | |Install: via source or PyPi      |     |     |
    | | |                                 |     |     |
    | | +---------------------------------+     |     |
    | +-----------------------------------------+     |
    +-------------------------------------------------+


## Structure
The folder structure for this project is as follows:

    .
    ├── .github                 # Github specific files (Github Actions workflows)
    ├── app                     # FastAPI app files for the API endpoints
    └── config                  # Config files for the Docker container

## Deployment
In order to run the docker container locally or non linux machines one needs to install [Docker Desktop](https://www.docker.com/products/docker-desktop) available for Mac and Windows

### API-only

In order to run a locally build version run:

```bash
docker-compose up --build
```

The API swagger documentation should now be available at [http://localhost:5000/docs/](http://localhost:5000/docs/).