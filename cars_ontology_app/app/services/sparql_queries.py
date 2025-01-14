from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings


def execute_sparql_query(query):
    """
    Helper function to execute a SPARQL query against the Fuseki server.
    """
    sparql = SPARQLWrapper(settings.FUSEKI_SPARQL_ENDPOINT)
    prefix = """PREFIX : <http://www.semanticweb.org/janbi/ontologies/2025/0/cars-ontology/>\n
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"""
    query = prefix + "\n" + query
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def fetch_filtered_listings(
    brand=None,
    model=None,
    engine=None,
    transmission=None,
    model_version_type=None,
    min_price=None,
    max_price=None,
    car_state=None,
):
    filters = []

    if brand and brand != "All":
        filters.append(
            f'?model :isManufacturedBy ?manufacturer . ?manufacturer :hasManufacturerName "{brand}" .'
        )
    if model and model != "All":
        filters.append(f'?model :hasModelName "{model}" .')
    if engine and engine != "All":
        filters.append(f"?car :hasEngine ?engine . ?engine rdf:type :{engine} .")
    if transmission and transmission != "All":
        filters.append(
            f"?car :hasTransmission ?transmission . ?transmission rdf:type :{transmission} ."
        )
    if model_version_type and model_version_type != "All":
        filters.append(f'?modelVersion :hasType "{model_version_type}" .')
    if min_price:
        filters.append(f"?listing :hasPrice ?price . FILTER(?price >= {min_price}) .")
    if max_price:
        filters.append(f"?listing :hasPrice ?price . FILTER(?price <= {max_price}) .")
    if car_state and car_state != "All":
        filters.append(f'FILTER(?carState = "{car_state}") .')

    filter_string = "\n".join(filters)

    query = f"""
        SELECT ?title ?modelVersionName ?modelName ?manufacturerName ?postedDate ?expiryDate ?description ?mileage ?price 
               (STRAFTER(STR(?transmissionType), "cars-ontology/") AS ?transmissionTypeName) ?transmissionName ?numberOfGears 
               (STRAFTER(STR(?engineType), "cars-ontology/") AS ?engineTypeName) ?engineName ?volume ?horsePower ?countryOfOrigin
               ?vin ?year ?address ?city ?country ?zipCode 
               (STRAFTER(STR(?sellerType), "cars-ontology/") AS ?sellerTypeName) ?sellerName ?taxId ?modelVersionType ?carState WHERE {{
            ?listing a :Listing ;
                :hasTitle ?title ;
                :isListingOf ?car ;
                :hasPostedDate ?postedDate ;
                :hasExpiryDate ?expiryDate ;
                :hasDescription ?description ;
                :hasPrice ?price ;
                :locatedAt ?location ;
                :listedBy ?seller .
            ?car :hasModelVersion ?modelVersion ;
                 :hasMileage ?mileage ;
                 :hasTransmission ?transmission ;
                 :hasEngine ?engine ;
                 :hasVIN ?vin ;
                 :hasYear ?year ;
                 :hasCarOriginCountry ?countryOfOrigin .
            ?modelVersion :isVersionOfModel ?model ;
                          :hasModelVersionName ?modelVersionName ;
                          :hasType ?modelVersionType .
            ?model :hasModelName ?modelName ;
                   :isManufacturedBy ?manufacturer .
            ?manufacturer :hasManufacturerName ?manufacturerName .
            ?transmission rdf:type ?transmissionType ;
                          :hasTransmissionName ?transmissionName ;
                          :hasNumberOfGears ?numberOfGears .
            ?transmissionType rdfs:subClassOf :Transmission .
            ?engine rdf:type ?engineType ;
                    :hasEngineName ?engineName ;
                    :hasVolume ?volume ;
                    :hasHorsePower ?horsePower .
            ?engineType rdfs:subClassOf :Engine .
            ?location :hasAddress ?address ;
                      :hasCity ?city ;
                      :hasCountry ?country ;
                      :hasZIPCode ?zipCode .
            ?seller rdf:type ?sellerType ;
                    :hasSellerName ?sellerName .
            ?sellerType rdfs:subClassOf :Seller .
            OPTIONAL {{
                ?seller a :Dealership ;
                        :hasTaxId ?taxId .
            }}
            BIND(IF(EXISTS {{ ?car a :NewCar }}, "New", "Used") AS ?carState)
            {filter_string}
        }}
    """
    results = execute_sparql_query(query)
    listings = []
    for result in results["results"]["bindings"]:
        listing = {
            "title": result["title"]["value"],
            "modelName": result["modelName"]["value"],
            "modelVersionName": result["modelVersionName"]["value"],
            "manufacturerName": result["manufacturerName"]["value"],
            "postedDate": result["postedDate"]["value"],
            "expiryDate": result["expiryDate"]["value"],
            "description": result["description"]["value"],
            "mileage": result["mileage"]["value"],
            "price": result["price"]["value"],
            "transmissionType": result["transmissionTypeName"]["value"],
            "transmissionName": result["transmissionName"]["value"],
            "numberOfGears": result["numberOfGears"]["value"],
            "engineType": result["engineTypeName"]["value"],
            "engineName": result["engineName"]["value"],
            "volume": result["volume"]["value"],
            "horsePower": result["horsePower"]["value"],
            "vin": result["vin"]["value"],
            "year": result["year"]["value"],
            "countryOfOrigin": result["countryOfOrigin"]["value"],
            "address": result["address"]["value"],
            "city": result["city"]["value"],
            "country": result["country"]["value"],
            "zipCode": result["zipCode"]["value"],
            "sellerType": result["sellerTypeName"]["value"],
            "sellerName": result["sellerName"]["value"],
            "modelVersionType": result["modelVersionType"]["value"],
            "carState": result["carState"]["value"],
        }
        if "taxId" in result:
            listing["taxId"] = result["taxId"]["value"]
        listings.append(listing)
    return listings


def fetch_all_listings():
    query = """
        SELECT ?title ?modelVersionName ?modelName WHERE {
                    ?listing a :Listing ;
                        :hasTitle ?title ;
                        :isListingOf ?car .
                    ?car :hasModelVersion ?modelVersion .
                    ?modelVersion :isVersionOfModel ?model .
                    ?model :hasModelName ?modelName .
                    ?modelVersion :hasModelVersionName ?modelVersionName .
        }
    """
    results = execute_sparql_query(query)
    listings = []
    for result in results["results"]["bindings"]:
        listings.append(
            {
                "title": result["title"]["value"],
                "modelName": result["modelName"]["value"],
                "modelVersionName": result["modelVersionName"]["value"],
            }
        )
    return listings


def fetch_all_manufacturers():
    query = """
        SELECT ?manufacturerName WHERE {
            ?manufacturer a :Manufacturer ;
                :hasManufacturerName ?manufacturerName .
        }
    """
    results = execute_sparql_query(query)
    manufacturers = []
    for result in results["results"]["bindings"]:
        manufacturers.append(result["manufacturerName"]["value"])
    return manufacturers


def fetch_all_models():
    query = """
        SELECT ?modelName WHERE {
            ?model a :Model ;
                :hasModelName ?modelName .
        }
    """
    results = execute_sparql_query(query)
    models = []
    for result in results["results"]["bindings"]:
        models.append(result["modelName"]["value"])
    return models


def fetch_all_transmission_types():
    query = """
        SELECT DISTINCT (STRAFTER(STR(?transmissionType), "cars-ontology/") AS ?transmissionName) WHERE {
        ?car :hasTransmission ?transmission .
        ?transmission rdf:type ?transmissionType .
        ?transmissionType rdfs:subClassOf :Transmission .
    }
    """
    results = execute_sparql_query(query)
    transmissions = []
    for result in results["results"]["bindings"]:
        transmissions.append(result["transmissionName"]["value"])
    return transmissions


def fetch_all_engine_types():
    query = """
        SELECT DISTINCT (STRAFTER(STR(?engineType), "cars-ontology/") AS ?engineName) WHERE {
        ?car :hasEngine ?engine .
        ?engine rdf:type ?engineType .
        ?engineType rdfs:subClassOf :Engine .
    }
    """
    results = execute_sparql_query(query)
    engines = []
    for result in results["results"]["bindings"]:
        engines.append(result["engineName"]["value"])
    return engines


def fetch_all_model_version_types():
    query = """
        SELECT DISTINCT ?modelVersionType WHERE {
        ?modelVersion :hasType ?modelVersionType .
    }
    """
    results = execute_sparql_query(query)
    model_version_types = []
    for result in results["results"]["bindings"]:
        model_version_types.append(result["modelVersionType"]["value"])
    return model_version_types


def get_price_range():
    query = """
        SELECT (MIN(?price) AS ?minPrice) (MAX(?price) AS ?maxPrice) WHERE {
            ?listing a :Listing ;
                :hasPrice ?price .
        }
    """
    results = execute_sparql_query(query)
    min_price = float(results["results"]["bindings"][0]["minPrice"]["value"])
    max_price = float(results["results"]["bindings"][0]["maxPrice"]["value"])
    return min_price, max_price
