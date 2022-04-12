This docker container captures a python script build on the WikidataIntegrator library. 

The workflow copies an item from wikidata and stores the equivalent on the target wikibase and adds a mapping to the source item on Wikidata

1. It creates a property on the target wikibase that captures a mapping to the equivalent property in wikidata.
   
2. It fetches all properties from Wikidata and creates the equivalent property in the target Wikibase. To maintain consistency with the Wikidata property (semantic)
data model, for each created property a mapping to that source property in Wikidata is added. Here the property created in step 1 is used. 
   
# Steps to transfer Wikidata items to Wikibase
First build the docker container based on the Docker file in this folder. 

`docker build -t transferqid-latest .`

Run the following command to copy Wikidata properties to the target Wikibase
`docker run --network=host --env WIKIBASE=127.0.0.1 --env WBUSER=WikibaseAdmin --env WBPASS=WikibaseDockerAdminPass --env QID=Q29005901,Q30314624,Q29006144,Q97576324,Q3655009,Q28209017,Q47521925,Q422226,Q28209568,Q29005907,Q29006616,Q28890051,Q29006671 --env LANGUAGES=en,nl,fr,es,de -it transferqid-latest`

### arguments 
* `--network=host` To allow communication between different docker containers on the same host
* `--env WIKIBASE=127.0.0.1` Environment variable indicating the IP of the target Wikibase
* `--env WBUSER=` Username with botpermission on the target Wikibase
* `--env WBPASS=` Password
* `--env QID` Set of wikidata identifiers/qids separated by a comma, to those items that need to be copied to the target wikibase
* `--env LANGUAGES` Set of languages for the labels/descriptions and aliases that need to be transfered to the target wikibase. 
