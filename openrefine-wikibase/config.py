
"""
This file defines a few constants which configure
which Wikibase instance and which property/item ids
should be used
"""

# Endpoint of the MediaWiki API of the Wikibase instance
mediawiki_api_endpoint = 'http://wikibase.svc/w/api.php'

# SPARQL endpoint
wikibase_sparql_endpoint = 'http://wdqs.svc:9999/bigdata/namespace/wdq/sparql'

# Name of the Wikibase instance
wikibase_name = 'Wikidata MVP'

# URL of the main page of the Wikibase instance
wikibase_main_page = 'http://wikibase.svc/wiki/Main_Page'

# Wikibase namespace ID, used to search for items
# For Wikidata this is 0, but most by default Wikibase uses 120, which is the default Wikibase 'Item:' namespace
# CHANGE THIS TO 120 if you are adapting this configuration file to another Wikibase
wikibase_namespace_id = 0

# Namespace prefix of Wikibase items (including colon, e.g. 'Item:')
wikibase_namespace_prefix = ''

# User agent to connect to the Wikidata APIs
user_agent = 'OpenRefine-Wikidata reconciliation interface'

# Regexes and group ids to extracts Qids and Pids from URLs
import re
q_re = re.compile(r'(<?https?://wikibase.svc/(entity|wiki)/)?(Q[0-9]+)>?')
q_re_group_id = 3
p_re = re.compile(r'(<?https?://wikibase.svc/(entity/|wiki/Property:))?(P[0-9]+)>?')
p_re_group_id = 3

# Identifier space and schema space exposed to OpenRefine.
# This should match the IRI prefixes used in RDF serialization.
# Note that you should be careful about using http or https there,
# because any variation will break comparisons at various places.
identifier_space = 'http://wikibase.svc/entity/'
schema_space = 'http://wikibase.svc/prop/direct/'

# Pattern used to form the URL of a Qid.
# This is only used for viewing so it is fine to use any protocol (therefore, preferably HTTPS if supported)
qid_url_pattern = 'http://wikibase.svc/wiki/{{id}}'

# By default, filter out any items which are instance
# of a subclass of this class.
# For Wikidata, this is "Wikimedia internal stuff".
# This filters out the disambiguation pages, categories, ...
# Set to None to disable this filter
avoid_items_of_class = 'Q17442446'


# Service name exposed at various places,
# mainly in the list of reconciliation services of users
service_name = 'Wikidata MVP Service'

# URL (without the trailing slash) where this server runs
this_host = 'http://localhost:8000'

# The default limit on the number of results returned by us
default_num_results = 25

# The maximum number of search results to retrieve from the Wikidata search API
wd_api_max_search_results = 50 # need a bot account to get more

# The matching score above which we should automatically match an item
validation_threshold = 95

# Redis client used for caching at various places
redis_uri = 'redis://redis:6379/0?encoding=utf-8'

# Redis prefix to use in front of all keys
redis_key_prefix = 'openrefine_wikidata:'

# Headers for the HTTP requests made by the tool
headers = {
    'User-Agent':service_name + ' (OpenRefine-Wikibase reconciliation service)',
}

# Previewing settings

# Dimensions of the preview
zoom_ratio = 1.0
preview_height = 100
preview_width = 400

# With which should be requested from Commons for the thumbnail
thumbnail_width = 130

# All properties to use to get an image. Set to empty list [] if no image properties are available.
image_properties = []

# URL pattern to retrieve an image from its filename
image_download_pattern = 'https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/%dpx-%s'

# Fallback URL of the image to use when previewing an item with no image
fallback_image_url = this_host + '/static/wikidata.png'

# Alt text of the fallback image
fallback_image_alt = 'Wikidata'

# Autodescribe endpoint to use.
# this is used to generate automatic descriptions from item contents.
# (disable this with: autodescribe_endpoint = None )
autodescribe_endpoint = None

# Property proposal settings

# Default type : entity (Q35120)
# Set to None if so such item exists.
# TODO: Update to the current QID from your Wikibase that match Q35120 on https://www.wikidata.org/wiki/Q35120
default_type_entity = 'Q83'

# Property path used to obtain the type of an item
# TODO: Update P31 with the value from your Wikibase
type_property_path = 'P147'

# Property to follow to fetch properties for a given type.
# Set to None if this is not available
# TODO: Update P1963 with the value from your Wikibase
property_for_this_type_property = 'P3154'

# Optional prefix in front of properties in SPARQL-like property paths
wdt_prefix = 'wdt:'

# Sparql query used to fetch all the subclasses of a given item.
# The '$qid' string will be replaced by the qid whose children should be fetched.
# TODO: Update P279 with the value from your Wikibase
sparql_query_to_fetch_subclasses = """
SELECT ?child WHERE { ?child wdt:P435* wd:$qid }
"""

# Sparql query used to fetch all the properties which store unique identifiers
# TODO: Update P31, P279 and https://www.wikidata.org/wiki/Q19847637 with the value from your Wikibase
sparql_query_to_fetch_unique_id_properties = """
SELECT ?pid WHERE { ?pid wdt:P147/wdt:P435* wd:Q71 }
"""

# Sparql query used to propose properties to fetch for items of a given class.
# Set to None if property proposal should be disabled.
# TODO: Update P279 with the value from your Wikibase
sparql_query_to_propose_properties = """
SELECT ?prop ?propLabel ?depth WHERE {
SERVICE gas:service {
    gas:program gas:gasClass "com.bigdata.rdf.graph.analytics.BFS" .
    gas:program gas:in wd:$base_type .
    gas:program gas:out ?out .
    gas:program gas:out1 ?depth .
    gas:program gas:maxIterations 10 .
    gas:program gas:maxVisited 100 .
    gas:program gas:linkType wdt:P435 .
}
SERVICE wikibase:label { bd:serviceParam wikibase:language "$lang" }
?out wdt:$property_for_this_type ?prop .
}
ORDER BY ?depth
LIMIT $limit
"""