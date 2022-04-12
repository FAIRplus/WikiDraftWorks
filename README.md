# Minimal Viable Wikibase (MVP)
This document describe the step involved in getting Wikibase running in a set of containers working in concertation. 

## Version 1.0.0
To track version [Semantic Versioning](https://semver.org/) is applied.

## Contents
This runbook contains:
* [steps to deploy a minimal viable Wikibase stack. This contains the core Wikibase stack (including the Blazegraph RDF store)](INSTALL_WB.md). 
* [instructions on how to run a script (dockerized) to import the properties from Wikidata.](wikidata-property-tranfer/README.md) 
* [instructions on how to replicate an item from Wikidata on this Wikibase, while maintaining its provenance.]( copy-wikidata-wikibase/README.md)


## Step by steps for deployment

### Main containers

1. `docker-compose up --build --no-start novartis-openrefine`
2. `docker-compose up -d`
3.  Review containers: `docker stats`
    * 11 containers needs to be running

### Property transfer (Run only one time per deployment) 
4. `cd wikidata-property-tranfer`
5. `docker-compose up --build --no-start`
6. `docker-compose up` (take a while to execute)
7. `cd ..` (Go back to the main containers)
8. `docker-compose stop`
9. `docker-compose up`
10. Review all properties are listed on the Wikibase: http://localhost:8181/wiki/Special:ListProperties

### Copy data from Wikidata to docker Wikibase

11. `cd copy-wikidata-wikibase`
12. `docker-compose up --build --no-start`
13. `docker-compose up` (take a while to execute)
    * Configure the QID to copy in the `docker-compose.yml` on this folder with environment variable `QID`
    * In case of errors run again `docker-compose up` until the last QID is loaded
    
### Configure openrefine-wikibase server

14. Open Wikibase query service: http://localhost:8282
15. Run query to get the values for the following step: 
    ```
    SELECT * WHERE {
    VALUES ?wikidata {<http://www.wikidata.org/entity/P31> <http://www.wikidata.org/entity/P279> <http://www.wikidata.org/entity/P1963> }
    ?wikibase <http://wikibase.svc/prop/direct/P1> ?wikidata ;
    rdfs:label ?label .
    }
    ```
16. Update values in `openrefine-wikibase/config.py` for all `TODO` values
17. `docker-compose stop reconcile`
18. `docker-compose up --build --no-start reconcile`
19. `docker-compose up -d`
20. `docker-compose exec wikibase php /var/www/html/maintenance/runJobs.php` (take a while to execute)
21. Check that the Wikibase API returns some results from http://localhost:8181/w/api.php?action=wbsearchentities&format=json&language=en&limit=50&search=Votubia
22. You can use OpenRefine to reconcile data with:
    * Wikibase Reconciliation Endpoint: http://localhost:8000/en/api
    * Wikibase Query Service SPARQL Endpoint: http://localhost:8989/bigdata/namespace/wdq/sparql


## Endpoints for all services

* Wikibase: http://localhost:8181
* Wikibase API: http://localhost:8181/w/api.php
* Wikibase Query Service: http://localhost:8282
* Wikibase Query Service SPARQL Endpoint: http://localhost:8989/bigdata/namespace/wdq/sparql
* Wikibase Reconciliation: http://localhost:8000
* Wikibase Reconciliation Endpoint: http://localhost:8000/en/api
* OpenRefine: http://localhost:3333/

