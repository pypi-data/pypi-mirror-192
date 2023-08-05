
# Instructions to add new queries: 
# Create new function, document correctly its parameter(s), replace the parameter name(s) as ##INPUT[I]## in the sparql query. 
# TODO: keep queury in the result file to keep track 
# TODO: uniformize arguments and name of fields (e.g. `slug` = 'short name' in all function)
# TODO: __init__ that raises an error when used withotu function and tells to select a query (for instance, printing all available functions). 

from .utils import replace_input, attr, setRecursive, setNonRecursive

class getSparqlQuery: 
    """
    Available SPARQL queries.
    
    This class is used to store functions that generate SPARQL queries. All functions return queries as a string to use with `query_from_sparql` but do not run any query on a triplestore endpoint at this point. 
    
    Returns: 
        A string which contains a SPARQL command to use with `query_from_sparql`.
        Additionally, the string will store a 'isRecursive' attribute (boolean) for some queries to be iterated over their own output. 
    
    """

    def all_triples(order_by = "s", n = 10): 
        """
        Shows all triples. 

        Args: 
            order_by (str): how to order the output. "s", "p", or "o". 
            n (int): how many triples to show.
        
        """
        query = """
        SELECT *
        WHERE {
            ?s ?p ?o
        }
        ORDER BY ?##INPUT0##
        LIMIT ##INPUT1##
        """
        replace_by = [order_by, str(n)]
        query = replace_input(query, replace_by)
        query = attr(query,'isRecursive', setNonRecursive)
        return(query)
    

    def datasets_from_keyword(keyword): 
        """
        Retrieves datasets associated to a project's keyword, also showing original project or imported/modified

        Args: 
            keyword (str): A project's keyword, e.g. "omni_batch_processed".
        Returns: 
            `query`: the query, project's keyword
            `dsName`: dataset name 
            `dsIdentifier`: dataset ID
            `originalDsId`: ID of the original dataset that was imported.
            `previousVersionDsId`: ID of the datasets that were imported in duplicate.         
        """
        query = """
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX renku: <https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX schema: <http://schema.org/>

        SELECT DISTINCT ?query ?dsName ?dsIdentifier ?originalDsId ?previousVersionDsId 
        WHERE {
        ?projectId a schema:Project;
                    schema:name '##INPUT0##';
                    schema:name ?query;
                    renku:hasDataset ?dsId.  
                    ## all hadDataset IDs related to project
        ?dsId schema:name ?dsName;
                schema:identifier ?dsIdentifier. 
                ## identifier from triples where hadDataset IDs are the subject
        OPTIONAL { ?dsId prov:wasDerivedFrom/schema:url ?previousVersionDsId } ## <-- for old datasets that were reused
        }
        order by (?dsName)
        """
        query = replace_input(query, [keyword])
        query = attr(query,'isRecursive', setNonRecursive)
        return(query)

    def name_from_keyword(keyword): 
        """
        Retrieves dataset name (`name`) and pseudoname (`slug`) from its keyword.

        Args: 
            keyword (str): A project name, e.g. 'omni_batch'.
        Returns: 
            `query`: the query, `keyword` 
            `name`
            `slug` 
        
        """

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT DISTINCT ?query ?slug ?name 
        WHERE {
        ?x ns3:keywords '##INPUT0## .
        ?x ns2:slug ?slug .
        ?x ns3:keywords ?query .
        ?x ns3:name ?name .
        ?x ns3:hasPart ?hasPart .
            } 
        """
        query = replace_input(query, [keyword])
        query = attr(query,'isRecursive', setNonRecursive)
        return(query)

    def ID_from_name(ds_name): 
        """
        Retrieves dataset IDs (`identifier` and `originalIdentifier`) of a dataset.

        Args: 
            ds_name (str): A dataset name, e.g. 'Standardized CellBench dataset - omni_batch'.
        Returns: 
            `query`: the query, `ds_name`
            `originalIdentifier`
            `identifier`
        
        """

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?query ?ID ?originalIdentifier
        WHERE {
                ?x ns3:name "##INPUT0##" .
                ?x ns3:name ?query .
                ?x ns2:originalIdentifier ?originalIdentifier .
                ?x ns1:wasDerivedFrom ?wasDerivedFrom .
            ?x ns3:identifier ?ID .
            } 
        """
        query = replace_input(query, [ds_name])
        query = attr(query,'isRecursive', setNonRecursive)
        return(query)

    
    def name_from_keyword(keyword): 
        """
        Retrieves the short name of the projects linked to a given keyword. 

        Args: 
            ds_name (str): A dataset name, e.g. 'Standardized CellBench dataset - omni_batch'.
        Returns: 
            `query`: the query, `ds_name`
            `slug`: the short name of the project. 
            `name`: the full name of the project.
        
        """

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT DISTINCT ?query ?slug ?name 
        WHERE {
            ?x ns3:keywords '##INPUT0##' .
            ?x ns3:keywords ?query .
            ?x ns2:slug ?slug .
            ?x ns3:keywords ?keyword .
            ?x ns3:name ?name .
            ?x ns3:hasPart ?hasPart .
            } 
        """
        query = replace_input(query, [keyword])
        query = attr(query,'isRecursive', setNonRecursive)
        return(query)

    def files_from_keyword(keyword): 
        """
        Retrieves all files imported or produced by project(s) having a certain keyword.

        Args: 
            keyword (str): A project's short name, e.g. 'Standardized CellBench dataset - omni_batch'.
        Returns: 
            `query`: the query, `keyword` arg. 
            `slug`: the short name of the project. 
            `name`: the full name of the project.
        
        """

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT DISTINCT ?query ?file
        WHERE {
        ?x ns3:keywords '##INPUT0##' .
        ?x ns3:keywords ?query .
        ?x ns3:hasPart ?hasPart .
        ?hasPart ns3:isBasedOn ?isBasedOn .  
        ?isBasedOn ns1:atLocation ?file .
        }
        """
        query = replace_input(query, [keyword])
        query = attr(query,'isRecursive', setNonRecursive)
        return(query)

    #TODO: OPTIMIZE (also query l.155 of sparql_try.rq)
    def all_triplestore_datasets(): 
        """
        Retrieves all datasets in the triplestore. 

        Returns: 
            `name`: name of the datasets
            `OriginalProjectID`: project ID
            `descr`: description of the dataset
            `keyword`: keyword associated to the dataset. 
        """

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ex: <https://renkulab.io/dataset-files/>
        SELECT DISTINCT   ?name ?OriginProjectID ?descr ?slug ?keyword
        WHERE {
        ?projectId a ns3:Project;
                    ns3:name 'omni_batch_processed';  
                    ns3:name ?projectName;
                    ns2:hasDataset ?dsId.  
        ?dsID ns3:hasPart ?hasPart .
        ?hasPart ns1:entity ?entity .
        ?OriginProjectID ns1:entity ?entity .
        ?originID ns3:hasPart ?OriginProjectID .
        ?originID ns3:name ?name .
        ?originID ns3:description ?descr .
        ?originID ns2:slug ?slug .
        OPTIONAL { ?originID ns3:keyword ?keyword .}
        }
        """
        query = replace_input(query)
        query = attr(query,'isRecursive', setNonRecursive)
        return(query)

    def imported_datasets_from_project(project_name): 
        """
        Retrieves all datasets imported by a project.

        Args: 
            project_name (str): abbreviated name of the project, e.g. 'omni_batch_processed'
        Returns: 
            `query`: the query, `project_name`
            `full_name`: project full name
            `short_name`: project short name
            `keyword`: keyword associated to the dataset
            `creator`: the mail of the author of the dataset
            `dateCreated`
            `descr`: decription of the dataset
            `originID`: ID of dataset        
        """

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ex: <https://renkulab.io/dataset-files/>
        SELECT DISTINCT ?query ?full_name ?short_name ?keyword ?creator ?dateCreated ?descr ?originID
        WHERE {
        ?projectId a ns3:Project;
                    ns3:name '##INPUT0##';
                    ns3:name ?query;
                    ns2:hasDataset ?dsId.  
        ?dsId ns3:hasPart ?hasPart .
        ?dsId ns3:sameAs ?originalDsId .
        ?hasPart ns1:entity ?entity .
        ?OriginProjectID ns1:entity ?entity .    
        ?originID ns3:hasPart ?OriginProjectID .
        ?originID ns3:name ?full_name .
        ?originID ns2:slug ?short_name .
        ?originID ns3:keywords ?keyword .
        ?originID ns3:creator ?creator .
        ?originID ns3:dateCreated ?dateCreated .
        ?originID ns3:description ?descr . 
        FILTER  (!(?keyword IN ('##INPUT0##')))
        }
        """
        query = replace_input(query, [project_name])
        query = attr(query, 'isRecursive', setNonRecursive)
        return(query)

    def input_from_file(file, do_recursive = False): 
        ## TODO: add n_step if user don't want to go either full recursive or not recusrive at all?
        """
        Retrieves all files used as an input by a file (e.g. method result or processed file). By default, the function will do a recursive search. Note: the query will ignore any files in the `src` or `log` folders. 

        Args: 
            file (str): path to the file to query on, relative to the main directory of the project. E.g. 'data/omni_batch_mnn/cellbench_10_none_20_inverse_corrected_counts.mtx.gz'
            do_recursive (bol): perform the query recursively from the output, until the raw project ? 
        Returns: 
            `query`: the query, `file`
            `out`: the paths to the files used to generate the query file
            `url`: the URL to the project that hosts the `out` datafiles.   
        """

        # Get output folder path from file path
        file_dir=file.split("/")
        del file_dir[-1]
        file_dir='/'.join(file_dir)

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ex: <https://renkulab.io/dataset-files/>
        SELECT DISTINCT ?query ?out ?url 
        WHERE {
        ?projectId a ns1:Entity;
                    ns1:atLocation '##INPUT0##'; 
                    ns1:qualifiedGeneration ?Generation.
        ?projectId ns1:atLocation ?query .
        ?Generation ns1:activity ?activity .
        ?activity ns2:parameter ?params .
        ?params ns3:value ?out .
        FILTER (!regex (?out, "##INPUT1##", "i"))  
        FILTER (!regex (?out, "^src/", "i"))  
        FILTER (!regex (?out, "^log/", "i"))
        ?pointer ns1:atLocation ?out .
        ?pointer ns3:url ?url .
        
        }
        
        """
        query = replace_input(query, [file, file_dir])
        if do_recursive: 
            query = attr(query, 'isRecursive', setRecursive)
            query = attr(query, 'isRecursive', setRecursive)
        else: 
            query = attr(query, 'isRecursive', setNonRecursive)
        return(query)

    ## TODO: add a `project_from_file` function doing a cross repo such as above from query line ~245 but fix it. 
    ## problem with the query, that fetches the processed file from parallel project (MNN when querying on harmony, because MNN also uses the processed fiels)

    def parameters_from_file(file, params_only = False): 
        """
        Retrieves all parameters and input used to generate a file (e.g. method result or processed file). 

        Args: 
            file (str): path to the file to query on, relative to the main directory of the project. E.g. 'data/omni_batch_mnn/cellbench_10_none_20_inverse_corrected_counts.mtx.gz'
            params_only (bol): only return parameters and filter out datasets used as input parameter ? 
        Returns: 
            `query`: the query, `file`
            `params`: the parameter value
            `paramName`: the parameter name, as used by the Renku plan
            `paramPrefix`: the prefix (usually a flag) used in combination with the parameter value
            `defaultValue`: the default value defined in the Renku plan 
        """

        # Get output folder path from file path
        file_dir=file.split("/")
        del file_dir[-1]
        file_dir='/'.join(file_dir)

        if params_only: 
            extra = "?paramRef rdf:type ns2:CommandParameter ."
        else: 
            extra = ""

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ex: <https://renkulab.io/dataset-files/>
        SELECT DISTINCT ?query ?params ?paramName ?paramPrefix ?defaultValue
        WHERE {
        ?projectId a ns1:Entity;
                    ns1:atLocation '##INPUT0##';  
                    ns1:qualifiedGeneration ?Generation.
        ?projectId ns1:atLocation ?query .
        ?Generation ns1:activity ?activity .
        ?activity ns2:parameter ?paramsID .
        ?paramsID ns3:value ?params .
        FILTER (!regex (?params, '##INPUT1##', "i"))  
        ?paramsID ns3:valueReference ?paramRef .
        ##INPUT2##
        ?paramRef ns3:name ?paramName .
        ?paramRef ns2:prefix ?paramPrefix .
        ?paramRef ns3:defaultValue ?defaultValue .
        }
        """
        query = replace_input(query, [file, file_dir, extra])
        query = attr(query, 'isRecursive', setNonRecursive)

        return(query)

    def plans_from_project(project_url): 
        """
        Retrieves plans (valid or not) associated to a project. 

        Args: 
            project_url (str): Renkulab URL to the project to query on.
        Returns: 
            `query`: the query, `project_url`
            `plan`: plan associated to the project
            `invalidatedAtTime`: if the project was invalidated, the time of the event. If valid, blank. 
            `dateCreated`
            `name`: name of the plan 
            `command`: command used with the plan
        """

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ex: <https://renkulab.io/dataset-files/>
        SELECT DISTINCT ?query ?plan ?invalidatedAtTime ?dateCreated ?name ?command
        WHERE {
            ?query ?p ?o
            FILTER (regex( str( ?query ), '##INPUT0##','i')) 
            ?query ns2:hasPlan ?plan .
            OPTIONAL { ?plan ns1:invalidatedAtTime ?invalidatedAtTime } 
            ?plan ns3:dateCreated ?dateCreated . 
            ?plan ns3:name ?name . 
            ?plan ns2:command ?command . 
        }
        """
        query = replace_input(query, [project_url])
        query = attr(query,'isRecursive', setNonRecursive)
        return(query)

    def activities_from_project(project_url, show_details = False): 
        """
        Retrieves activities (and related plans) associated to a project. 

        Args: 
            project_url (str): Renkulab URL to the project to query on.
            show_details (bol): whether to show the files associated with the activities. Enabling it will considerably increase the size of the output. 
        Returns: 
            `query`: the query, `project_url`
            `plan`: plan associated to the project
            `invalidatedAtTime`: if the project was invalidated, the time of the event. If valid, blank. 
            `activity`: the activity URL 
            `startTime`
            `endTime`
            `file`: if specified by `show_details`, the file related by the activity
            `paramValue`: if specified by `show_details`, the parameters used by the activity. 
        """

        if show_details: 
            extra = '?file ?paramValue'
        else: 
            extra = ''

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ex: <https://renkulab.io/dataset-files/>
        SELECT DISTINCT ?query ?plan ?invalidatedAtTime ?activity ?startTime ?endTime ##INPUT1## 
        WHERE {
            ?query ?p ?o
            FILTER (regex( str( ?query ), '##INPUT0##','i'))
            ?query ns2:hasPlan ?plan .
            OPTIONAL { ?plan ns1:invalidatedAtTime ?invalidatedAtTime } 
            ?assoc ns1:hadPlan ?plan .
            ?activity ns1:qualifiedAssociation ?assoc .
            ?activity ns1:startedAtTime ?startTime .
            ?activity ns1:endedAtTime ?endTime .
            # entities: input of the activity
            ?activity ns1:qualifiedUsage ?usage .
            ?usage ns1:entity ?entity .
            ?entity ns1:atLocation ?file .
            # parameters of the activity
            ?activity ns2:parameter ?params .
            ?params ns3:value ?paramValue .
        }
        """
        query = replace_input(query, [project_url, extra])
        query = attr(query, 'isRecursive', setNonRecursive)
        return(query)

    def project_from_file(file): 
        """
        Retrieves the information about the *original* project that created a file. 

        Args: 
            file (str): path to the file to query on, relative to the main directory of the project. E.g. 'data/omni_batch_mnn/cellbench_10_none_20_inverse_corrected_counts.mtx.gz'
        Returns: 
            `query`: the query, `file`
            `project_name`
            `project_link`: Renkulab URL to the project
            `dateCreated`
        """

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ex: <https://renkulab.io/dataset-files/>
        SELECT DISTINCT ?query ?project_name ?project_link ?dateCreated
        WHERE {
        ?projectId a ns1:Entity;
                    ns1:atLocation '##INPUT0##'; 
                    ns1:qualifiedGeneration ?Generation.
        ?projectId ns1:atLocation ?query .
        ?Generation ns1:activity ?activity .
        ?activity ns2:parameter ?params .
        ?project_link ns2:hasActivity ?activity . 
        ?project_link ns3:name ?project_name .
        ?project_link ns3:dateCreated ?dateCreated .
        }
        """
        query = replace_input(query, [file])
        return(query)

    def activity_from_file(file): 
        """
        Retrieves the activity linked to a file. 

        Args: 
            file (str): path to the file to query on, relative to the main directory of the project. E.g. 'data/omni_batch_mnn/cellbench_10_none_20_inverse_corrected_counts.mtx.gz'
        Returns: 
            `query`: the query, `file`
            `generation`
            `activity`
            `startTime`
            `endTime`
        """

        query = """
        PREFIX ns1:<http://www.w3.org/ns/prov#>
        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>
        PREFIX ns3:<http://schema.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ex: <https://renkulab.io/dataset-files/>
        SELECT DISTINCT  ?query ?generation ?activity ?startTime ?endTime
        WHERE {
        ?projectId a ns1:Entity;
                    ns1:atLocation '##INPUT0##'; 
                    ns1:qualifiedGeneration ?generation .
        ?projectId ns1:atLocation ?query .
        ?generation ns1:activity ?activity .
        ?activity ns1:startedAtTime ?startTime .
        ?activity ns1:endedAtTime ?endTime .
        }
        """
        query = replace_input(query, [file])
        return(query)


# ns3:name = 'full_name'
# ns2:slug = 'short_name
# ns3:keywords = 'keyword' 
# ns3:creator = 'creator' 
# dateCreated = 'dateCreated'
# ns3:description = 'descr' 
# originID = 'originID' 
# hasPlan = 'plan' 
# atLocation: file 


## TODO: put this into each function and allow to set number of step back. 
## will be handled by `query_from_sparql`
## Set True for : `input_from_file`
#attr()


#a=attr("aaaa",'isRecursive',setRecursive)
# Value in 'a'
#a
# attr of 'a', True
#a.isRecursive()

#a=attr("aaaa",'isRecursive',setNonRecursive)
# Value in 'a'
#a
# attr of 'a', False
#a.isRecursive()


