This docker container captures a python script build on the WikidataIntegrator library. The workflow consists of two steps:
1. It creates a property on the target wikibase that captures a mapping to the equivalent property in Wikidata.
   
2. It fetches all properties from Wikidata and creates the equivalent property in the target Wikibase. To maintain consistency with the Wikidata property (semantic)
data model, for each created property a mapping to that source property in Wikidata is added. Here the property created in step 1 is used. 
   
caveat: The support of linguistic properties such as lexeme's in Wikidata is not yet supported in the dockerized version of Wikibase. These properties will not be copied and will lead to some error messages when running the docker container. These error messages can be ignored for now, but should be captured and logged in future version of this script. 

# Steps to transfer Wikidata properties to Wikibase
First build the docker container based on the Docker file in this folder. 
`sudo docker build -t wikidatapropertytransfer:0.1 .`

Run the following command to copy Wikidata properties to the target Wikibase 
`sudo docker run --network=host --env WIKIBASE=127.0.0.1 --env WBUSER=WikibaseAdmin --env WBPASS=WikibaseDockerAdminPass -it wikidatapropertytransfer:0.1 `
