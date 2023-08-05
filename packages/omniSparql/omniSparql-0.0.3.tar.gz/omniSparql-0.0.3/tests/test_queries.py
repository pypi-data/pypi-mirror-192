from omniSparql.queries import query_from_sparql

def test_query_from_sparql():
    "Tests the query function on dpbedia."
    sparql_query = """
    PREFIX dbo: <http://dbpedia.org/ontology/> 
    PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

    SELECT ?country ?city ?city_name
    WHERE {
        ?city rdf:type dbo:City ;
            foaf:name ?city_name ;
            dbo:country ?country .

        ?country foaf:name "Canada"@en .

        FILTER(langMatches(lang(?city_name), "en"))
    }
    ORDER BY ?city_name
    LIMIT 10

    """
    URL = "https://dbpedia.org/sparql"
    out = query_from_sparql(sparql_query, URL = URL)
    assert len(out) == 2, "Error with SPAQRL query function."

