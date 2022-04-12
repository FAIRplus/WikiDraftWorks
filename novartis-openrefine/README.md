# Novartis OpenRefine distribution

Custom docker image to run [OpenRefine](https://openrefine.org/) for Novartis. This configuration includes the following:

* `Dockerfile`: build image `novartis-openrefine:1.0` (Needs access to DockerHub and https://github.com/OpenRefine/OpenRefine/releases/download)
* `docker-compose.yml`: start, stop and easy configuration for docker image `novartis-openrefine:1.0`
* `or-configuration`: folder with OpenRefine default configuration and the following extensions (see below for details):
    * RDF Extension
    * NER Extension 
    * Workspace File Extension


## Running with docker

* Build the container: `docker build . -t novartis-openrefine:1.0`
* Run the container: `docker run -p 3333:3333 novartis-openrefine:1.0`
    * You can define a volume to persist the OpenRefine Workspace with: `docker run -v /home/USER/novartis-openrefine/data:/or/data -p 3333:3333 novartis-openrefine:1.0`
* Open http://127.0.0.1:3333 in your browser
* Stop the container with `ctrl + c` in the terminal that is running `docker run...`

### Enable/Disable create project options

During the `docker build ...` command you can set the following arguments to disable any menus from the `Create Project` page. By default, all options are enabled.

* **This Computer:** `docker build --build-arg THIS_COMPUTER=false`
* **Web Addresses (URLs):** `docker build --build-arg WEB_ADDRESSES=false`
* **Clipboard:** `docker build --build-arg CLIPBOARD=false`
* **Database:** `docker build --build-arg DATABASE=false`
* **Workspace Data:** `docker build --build-arg WORKSPACE=false`
* **Google Data:** `docker build --build-arg GOOGLE=false`

**Example command to disable the Clipboard and the Workspace Data options** 
* `docker build --build-arg CLIPBOARD=false --build-arg WORKSPACE=false . -t novartis-openrefine:1.0`

## Running with docker-compose

* Build the container: `docker build . -t novartis-openrefine:1.0`
* Start the container: `docker-compose up -d`
* Open http://127.0.0.1:3333 in your browser  
* Stop the container: `docker-compose stop`

**Note:** additional configuration can be added/updated in `docker-compose.yml`

## OpenRefine Memory allocation

* Update values in `refine.ini` for variables `REFINE_MEMORY` and `REFINE_MIN_MEMORY` 
* Re-create the container `docker build . -t novartis-openrefine:1.0`

## Extension details and configuration

### RDF extension

#### Source Code: 

* [Public Repository on Github](https://github.com/stkenny/grefine-rdf-extension)
* [Novartis Repository Image]()

#### Version compiled in this docker image:

* Compilation date: 2021-01-29
* Compiled by: RefinePro
* Version 1.3.1 - non-official including [PR #58 Remove absolute URL for `command/core/load-language` request](https://github.com/stkenny/grefine-rdf-extension/pull/58)
* Commit reference to NVS rep:

#### Update Docker

When new development are made on the public repository:

* Pull the changes to Novartis repository image and resolve potential conflicts with other customization made.
* Compile and update the docker image (zip file and readme)

When patches are prepared by RefinePro: 

* Prepare the patch on RefinePro fork
* Send a pull request to the public repository
* Push to code the NVS repository 
* Compile and update the docker image (zip file and readme)

### NER extension

#### Source Code: 

* [Public Repository on Github](https://github.com/stkenny/Refine-NER-Extension)
* [Novartis Repository Image]()

#### Version compiled in this docker image:

* Compilation date: 2021-01-24
* Compiled by: stkenny
* [Version 1.6.1](https://github.com/stkenny/Refine-NER-Extension/releases/tag/v1.6.1)
* Commit reference to NVS rep: 

#### Update Docker

When new development are made on the public repository:

* Pull the changes to Novartis repository image and resolve potential conflicts with other customization made.
* Compile and update the docker image (zip file and readme)

When patches are prepared by RefinePro: 

* Prepare the patch on RefinePro fork
* Send a pull request to the public repository
* Push to code the NVS repository 
* Compile and update the docker image (zip file and readme)

### Workspace File extension

#### Source Code: 

* [Private Repository on RefinePro BitBucket](https://bitbucket.org/refinepro_team/openrefine-local-file-extension)
* [Novartis Repository Image]()

#### Version compiled in this docker image:

* Compilation date: 2021-01-04
* Compiled by: RefinePro
* Version 1.0.1 
* Commit reference to NVS rep: 

#### Update Docker

* RefinePro develop their private repository
* Push to code the NVS repository 
* Compile and update the docker image (zip file and readme)

#### Documentation: 

Location to load the files is configured with the environment variable `EXT_LOCAL_FILE_SYSTEM` in the `Dockerfile` archive and will load all files from folder `workspace-files`

* If you are running OpenRefine with `docker run...` adding/removing files in folder `workspace-files` requires a new build with `docker build . -t novartis-openrefine:1.0` to see the updates in OpenRefine.
* If you are running OpenRefine with `docker-compose ` adding/removing files in folder `workspace-files` will be reflected immediately as soon you refresh the page to create new projects 

## Acknowledgements

* The seed Dockerfile came from https://github.com/opencultureconsulting/openrefine-docker/blob/master/3.3/Dockerfile
