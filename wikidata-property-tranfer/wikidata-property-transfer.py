from wikidataintegrator import wdi_core, wdi_login
import os

from joblib import Parallel, delayed
import multiprocessing

if "WIKIBASE" in os.environ and "WBUSER" in os.environ and "WBPASS" in os.environ:
    WIKIBASE = os.environ["WIKIBASE"]
    WBUSER = os.environ['WBUSER']
    WBPASS = os.environ['WBPASS']
else:
    raise ValueError("WIKIBASE, WDUSER and WDPASS must be specified in local.py or as environment variables")

query = """
SELECT DISTINCT ?property ?propertyLabel ?propertyDescription ?propType WHERE {
   ?property wikibase:directClaim ?p ;
             wikibase:propertyType ?propType ;
             schema:description ?propertyDescription ;
             rdfs:label ?propertyLabel .
   FILTER (lang(?propertyLabel) = 'en')
   FILTER (lang(?propertyDescription) = 'en')}
"""
propertiesSparql = wdi_core.WDItemEngine.execute_sparql_query(query, as_dataframe=True)
datatype_map = {'http://wikiba.se/ontology#CommonsMedia': 'commonsMedia',
                'http://wikiba.se/ontology#ExternalId': 'external-id',
                'http://wikiba.se/ontology#GeoShape': 'geo-shape',
                'http://wikiba.se/ontology#GlobeCoordinate': 'globe-coordinate',
                'http://wikiba.se/ontology#Math': 'math',
                'http://wikiba.se/ontology#Monolingualtext': 'monolingualtext',
                'http://wikiba.se/ontology#Quantity': 'quantity',
                'http://wikiba.se/ontology#String': 'string',
                'http://wikiba.se/ontology#TabularData': 'tabular-data',
                'http://wikiba.se/ontology#Time': 'time',
                'http://wikiba.se/ontology#Url': 'url',
                'http://wikiba.se/ontology#WikibaseItem': 'wikibase-item',
                'http://wikiba.se/ontology#WikibaseLexeme': 'lexeme',
                'http://wikiba.se/ontology#WikibaseForm': 'form',
                'http://wikiba.se/ontology#WikibaseSense': 'sense',
                'http://wikiba.se/ontology#MusicalNotation': 'musical-notation',
                'http://wikiba.se/ontology#WikibaseProperty': 'wikibase-property'}
propertiesSparql['datatype']= ""
for index, row in propertiesSparql.iterrows():
  row["datatype"] = datatype_map[row["propType"]]

wikibase = "http://"+WIKIBASE+":8181/"
api = "http://"+WIKIBASE+":8181/w/api.php"
sparql = "http://"+WIKIBASE+":8282/proxy/wdqs/bigdata/namespace/wdq/sparql"
entityUri = wikibase.replace("https:", "http:")+"entity/"

login = wdi_login.WDLogin(WBUSER, WBPASS, mediawiki_api_url=api)

def get_properties():
    property_lookup = {}

    query = """
    SELECT ?property ?label
    WHERE {
        ?property a wikibase:Property .
        ?property rdfs:label ?label .
        FILTER (LANG(?label) = "en" )
    }"""

    results = wdi_core.WDItemEngine.execute_sparql_query(query=query, endpoint=sparql)

    for result in results["results"]["bindings"]:
        label = result["label"]["value"].split("/")[-1]
        property_lookup[label] = result["property"]["value"].split("/")[-1]

    return property_lookup

# Dictionary key = name of property, value = Pxxx
property_lookup = get_properties()

def createProperty(login=login, wdprop=None, label="", description="", property_datatype=""):
  if wdprop== None:
    s = []
  else:
    s = [wdi_core.WDUrl(wdprop, prop_nr="P1")]
  localEntityEngine = wdi_core.WDItemEngine.wikibase_item_engine_factory(api,sparql)
  item = localEntityEngine(data=s)
  item.set_label(label)
  item.set_description(description)
  print(item.write(login, entity_type="property", property_datatype=property_datatype))

#create mapping to wikidata property
if "property in wikidata" not in property_lookup:
  createProperty(login, label="property in wikidata", description="The same property in Wikidata", property_datatype="url")


datatype_map = {'http://wikiba.se/ontology#CommonsMedia': 'commonsMedia',
                'http://wikiba.se/ontology#ExternalId': 'external-id',
                'http://wikiba.se/ontology#GeoShape': 'geo-shape',
                'http://wikiba.se/ontology#GlobeCoordinate': 'globe-coordinate',
                'http://wikiba.se/ontology#Math': 'math',
                'http://wikiba.se/ontology#Monolingualtext': 'monolingualtext',
                'http://wikiba.se/ontology#Quantity': 'quantity',
                'http://wikiba.se/ontology#String': 'string',
                'http://wikiba.se/ontology#TabularData': 'tabular-data',
                'http://wikiba.se/ontology#Time': 'time',
                'http://wikiba.se/ontology#Url': 'url',
                'http://wikiba.se/ontology#WikibaseItem': 'wikibase-item',
                'http://wikiba.se/ontology#WikibaseProperty': 'wikibase-property'}

def createPropertyStage(row, property_lookup):
    if row.propertyLabel in property_lookup:
        pass
    else:
        try:
            createProperty(login=login, wdprop=row.property, label=row.propertyLabel,
                           description=row.propertyDescription, property_datatype=datatype_map[row.propType])
        except:
            print("Failed")

num_cores = multiprocessing.cpu_count()

results = Parallel(n_jobs=num_cores)(
    delayed(createPropertyStage)(i, property_lookup) for i in propertiesSparql.itertuples())

