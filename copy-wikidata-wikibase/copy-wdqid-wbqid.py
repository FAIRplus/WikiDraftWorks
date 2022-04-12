from wikidataintegrator import wdi_core, wdi_login 
from wikidataintegrator.wdi_config import config
import os
import time

if "LANGUAGES" in os.environ and "WIKIBASE" in os.environ and "WBUSER" in os.environ and "WBPASS" in os.environ and "QID" in os.environ:
    WIKIBASE = os.environ["WIKIBASE"]
    WBUSER = os.environ['WBUSER']
    WBPASS = os.environ['WBPASS']
    QID = os.environ['QID']
    languages = os.environ["LANGUAGES"].split(",")
else:
    raise ValueError(
        "LANGUAGES, WIKIBASE, WDUSER, WDPASS and QID must be specified in local.py or as environment variables")

wikibase = "http://" + WIKIBASE + ":8181/"
api = "http://" + WIKIBASE + ":8181/w/api.php"
sparql = "http://" + WIKIBASE + ":8282/proxy/wdqs/bigdata/namespace/wdq/sparql"
entityUri = wikibase.replace("https:", "http:") + "entity/"

login = wdi_login.WDLogin(WBUSER, WBPASS, mediawiki_api_url=api)

## The query below finds the property that captures the exact match property in the wikibase under scrutiny
exactmatchQuery = """PREFIX wbt: <http://wikibase.svc/prop/direct/>
          PREFIX wb: <http://wikibase.svc/entity/>
          PREFIX wd: <http://www.wikidata.org/entity/>
          SELECT * WHERE {
             ?localProp wikibase:directClaim ?property ;
                          wikibase:propertyType ?type ;
                          wbt:P1 wd:P2888}"""

emresults = wdi_core.WDItemEngine.execute_sparql_query(exactmatchQuery, endpoint=sparql)
em_property = emresults["results"]["bindings"][0]["property"]['value'].replace("http://wikibase.svc/prop/direct/", "")
em_property_url = emresults["results"]["bindings"][0]["property"]['value']

for wdid in QID.split(","):
    print(wdid, flush=True)  # The Wikidata item ID
    # create a parseable object for the Wikidata item under scrutiny
    wikidata_item = wdi_core.WDItemEngine(wd_item_id=wdid)
    content = wikidata_item.get_wd_json_representation()

    # From here the statements to be copied to the Wikibase will be built
    statements = []
    # First the mapping to Wikidata is set
    statements.append(wdi_core.WDUrl("http://www.wikidata.org/entity/" + wdid, prop_nr=em_property))

    # Iterate over the properties found in the wikidata item and captured above.
    for property in content["claims"].keys():
        # capture the Wikibase-Wikidata property mapping
        query = """PREFIX wbt: <http://wikibase.svc/prop/direct/>
                PREFIX wb: <http://wikibase.svc/entity/>
                PREFIX wd: <http://www.wikidata.org/entity/>
                SELECT * WHERE {{
               ?localProp wikibase:directClaim ?property ;
                          wikibase:propertyType ?type ;
                          wbt:P1 wd:{0} .}}""".format(property)
        results = wdi_core.WDItemEngine.execute_sparql_query(query,
                                                             endpoint=sparql)

        # Select the value types. Per value type a different json blob needs to be built to submit to the API
        # ExternalID
        if len(results["results"]["bindings"]) > 0:
            if results["results"]["bindings"][0]["type"]['value'] == "http://wikiba.se/ontology#ExternalId":
                for claim in content["claims"][property]:
                    statements.append(wdi_core.WDExternalID(claim['mainsnak']['datavalue']["value"],
                                                        prop_nr=results["results"]["bindings"][0]["localProp"][
                                                            'value'].replace("http://wikibase.svc/entity/", ""), ))
                
            # String
            if results["results"]["bindings"][0]["type"]['value'] == "http://wikiba.se/ontology#String":
                for claim in content["claims"][property]:
                    statements.append(wdi_core.WDString(claim['mainsnak']['datavalue']["value"],
                                                        prop_nr=results["results"]["bindings"][0]["localProp"][
                                                            'value'].replace("http://wikibase.svc/entity/", ""), ))
                
            # Monolingualtext

            if results["results"]["bindings"][0]["type"]['value'] == "http://wikiba.se/ontology#Monolingualtext":
                for claim in content["claims"][property]:
                    statements.append(wdi_core.WDMonolingualText(claim['mainsnak']['datavalue']["value"]["text"],
                                                        prop_nr=results["results"]["bindings"][0]["localProp"][
                                                            'value'].replace("http://wikibase.svc/entity/", ""), 
                                                             language=claim['mainsnak']['datavalue']["value"]["language"]))

            # Wikibase-item
            if results["results"]["bindings"][0]["type"]['value'] == "http://wikiba.se/ontology#WikibaseItem":
                for claim in content["claims"][property]:
                    mainsnak = claim['mainsnak']
                    if mainsnak["snaktype"] == "novalue":
                        statements.append(wdi_core.WDItemID(value=None, snak_type="novalue",
                                                        prop_nr=results["results"]["bindings"][0]["localProp"][
                                                            'value'].replace("http://wikibase.svc/entity/", "")))
                    else: 
                        temp_item = wdi_core.WDItemEngine(wd_item_id=mainsnak['datavalue']["value"]["id"])
                    
                    
                        query = "SELECT * WHERE {{?item <{0}> {1} .}}".format(em_property_url,
                                                                          "<http://www.wikidata.org/entity/" +
                                                                          mainsnak['datavalue']["value"][
                                                                              "id"] + ">")
                        temp_results = wdi_core.WDItemEngine.execute_sparql_query(query, endpoint=sparql)

                        if len(temp_results['results']['bindings']) == 0:
                            temp_statements = []
                            if mainsnak['datatype'] == 'wikibase-item':
                                temp_statements.append(
                                    wdi_core.WDUrl(
                                        "http://www.wikidata.org/entity/" + mainsnak['datavalue']['value']['id'],
                                        prop_nr=em_property))

                            temp_local_item = wdi_core.WDItemEngine(new_item=True, data=temp_statements, mediawiki_api_url=api, sparql_endpoint_url=sparql)
                        
                            for lang in languages:
                                temp_label = temp_item.get_label(lang=lang)
                                temp_description = temp_item.get_description(lang)
                        
                                temp_local_item.set_label(temp_label, lang=lang)
                                if temp_label != temp_description:
                                    temp_local_item.set_description(temp_description, lang=lang)         
                            local_qid = temp_local_item.write(login)
                        else:
                            local_qid = temp_results['results']['bindings'][0]["item"]["value"].replace("http://wikibase.svc/entity/", "")
                        statements.append(wdi_core.WDItemID(local_qid,
                                                        prop_nr=results["results"]["bindings"][0]["localProp"][
                                                            'value'].replace(
                                                            "http://wikibase.svc/entity/", "")))
    exist_query = """PREFIX wbt: <http://wikibase.svc/prop/direct/>
                PREFIX wb: <http://wikibase.svc/entity/>
                PREFIX wd: <http://www.wikidata.org/entity/>
                SELECT * WHERE {{
                     ?item wbt:{prop} wd:{value} .
                }}
                """.format(prop=str.rstrip(em_property), value=str.rstrip(wdid))
    results = wdi_core.WDItemEngine.execute_sparql_query(exist_query,
                                                         endpoint=sparql)

    if len(results["results"]["bindings"]) == 0:
        wikibase_item = wdi_core.WDItemEngine(new_item=True, data=statements,
                                              mediawiki_api_url=api,
                                              sparql_endpoint_url=sparql)
    else:
        wikibase_item = wdi_core.WDItemEngine(
            wd_item_id=results["results"]["bindings"][0]["item"]["value"].replace("http://wikibase.svc/entity/", ""),
            data=statements, mediawiki_api_url=api, sparql_endpoint_url=sparql)

    # labels
    # for language in content["labels"].keys():
    for language in languages:
        if language in content["labels"].keys():
            wikibase_item.set_label(content["labels"][language]['value'], lang=language)
    # descriptions
    # for language in content["descriptions"].keys():
    for language in languages:
        if language in content["descriptions"].keys():
            if content["descriptions"][language]['value'] != content["labels"][language]['value']:
                wikibase_item.set_description(content["descriptions"][language]['value'], lang=language)
    # alias
    if "alias" in content.keys():
        for language in content["alias"].keys():
            if language in languages:
                wikibase_item.set_aliases(content["alias"][language]['value'], lang=language)     
    try:
        print(wikibase_item.write(login), flush=True)
    except:
        print('error', flush=True)
