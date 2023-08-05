from omniSparql.sparql import getSparqlQuery

def test_query_from_sparql():
    "Tests if the sparql queries return a string without 'input' tag."
    
    # set functions without def args and a dummy arg to be sued
    no_def = {
        "datasets_from_project": "omni_batch_processed", 
        "random": "random" ## TODO: remove and replace with other queries
    }
    method_list = [method for method in dir(getSparqlQuery) if method.startswith('__') is False]

    for callable in method_list: 
        fun = getattr(getSparqlQuery, callable )
        if callable in list(no_def.keys()): 
            out = fun(no_def[callable])
        else: 
            out = fun()
        assert type(out) == str, "Error: output is not str."
        assert out.find("##INPUT") == -1, "Error: ##INPUT tag still here."
