
> [!IMPORTANT]
> On June 26 2024, Linux Foundation announced the merger of its financial services umbrella, the Fintech Open Source Foundation ([FINOS](https://finos.org)), with OS-Climate, an open source community dedicated to building data technologies, modeling, and analytic tools that will drive global capital flows into climate change mitigation and resilience; OS-Climate projects are in the process of transitioning to the [FINOS governance framework](https://community.finos.org/docs/governance); read more on [finos.org/press/finos-join-forces-os-open-source-climate-sustainability-esg](https://finos.org/press/finos-join-forces-os-open-source-climate-sustainability-esg)

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

For building the image the codes relies on source-to-image (s2i). Please install s2i first. the CLI can be found [here](https://github.com/openshift/source-to-image/releases/). Make sure the install location is added to the PATH variable.
```bash
s2i build . registry.access.redhat.com/ubi8/python-36 -e APP_FILE=app/main.py ofocp.azurecr.io/labs/itr-api:[YOUR_TAG] -c
```
- the build is based in the UBI 8 Python 3.6 base images.
- '-e APP_FILE=app/main.py' directs s2i to the applications that needs to run
- '-c' makes s2i build your local code version. When removed it will build the latest committed git stage


The API swagger documentation should now be available at [http://localhost:8080/docs/](http://localhost:8080/docs/).