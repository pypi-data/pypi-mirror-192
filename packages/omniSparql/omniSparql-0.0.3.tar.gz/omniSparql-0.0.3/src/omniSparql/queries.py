from SPARQLWrapper import SPARQLWrapper, JSON, XML, TURTLE, N3, RDF, RDFXML, CSV, TSV, JSONLD


def query_from_sparql(sparql_query, URL = "http://imlspenticton.uzh.ch/sparql", output_format = JSON): 
    """Runs a SPARQL query. 

    SPARQL queries can be retrieved from the `sparqlCollection` class.  

    Args: 
        sparql_query (str): a SPARQL command from TODO[define].
        URL (str): the URL to the triplestore.
        output_format (str): format of the output. One of SON, XML, TURTLE, N3, RDF, RDFXML, CSV, TSV, JSONLD. 
    
    Returns: 
        An output of the query, in the specified format. TODO [see if always dict_values]

    """
    
    sparql = SPARQLWrapper(URL)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(sparql_query)
    ret = sparql.queryAndConvert()
    return(ret['results']['bindings'])

 
# TODO: query_from_sparql for itererative, which needs the get_sparql_query function to modify it iteratively


