# omniSPARQL

`omniSparql` is a python module to query triples from the OMNIBENCHMARK triplestore. Its main usage is to retrieve lineage information in an OMNIBENCHMARK (see the [lineage query file](https://github.com/ansonrel/contributed-project-templates/blob/dev/metric_summary/src/generate_json_from_res_files.py) of summary metric projects).

## Usage

### Minimal usage

The typical use of `omniSparql` consists in forming a SPARQL based on your need and running it on your triplestore URL: 

```python
import omniSparql as omni
## get a query
query = omni.getSparqlQuery.CLASS_METHOD
## run the query 
out = omni.query_from_sparql(query, URL = TRIPLESTORE_URL)
```
### Detailled usage

Let's start by getting a query. Several SPARQL queries are available in the **`getSparqlQuery`** class, which you can explore with the `help` page of the page; 

```python
import omniSparql as omni
help(omni.getSparqlQuery)
```

```
Help on class getSparqlQuery in module omniSparql.sparql:

class getSparqlQuery(builtins.object)
 |  Available SPARQL queries. One or multiple input to define when called. 
 |  
 |  Returns: 
 |      A string which contains a SPARQL command to use with `query_from_sparql`.
 |  
 |  Methods defined here:

 [...]
 |  imported_datasets_from_project(project_name)
 |      Retrieves all datasets imported by a project.
 |      
 |      Args: 
 |          project_name (str): abbreviated name of the project, e.g. 'omni_batch_processed'
 |      Returns: 
 |          `query`: the query, `project_name`
 |          `full_name`: project full name
 |          `short_name`: project short name
 |          `keyword`: keyword associated to the dataset
 |          `creator`: the mail of the author of the dataset
 |          `dateCreated`
 |          `descr`: decription of the dataset
 |          `originID`: ID of dataset
 [...]

```

As an example, we can select the query showed above; `imported_datasets_from_project` and store it for the next step. As explained in the class method documentation, this function helps to identify which renku datasets were imported by a project, only by providing its name. Let's use it to query all datasets imported by one of the `iris` omnibenchmark; [`iris_accuracy`](https://renkulab.io/gitlab/omnibenchmark/iris_example/iris-accuracy) metric project.

Prepare the query: 

```python
q = omni.getSparqlQuery.imported_datasets_from_project(project_name='iris_accuracy')
q
```
```
"\n        PREFIX ns1:<http://www.w3.org/ns/prov#>\n        PREFIX ns2:<https://swissdatasciencecenter.github.io/renku-ontology#>\n        PREFIX ns3 [...]"
```

The output of any SPARQL query from `getSparqlQuery` can be used to query a specified triplestore with the **`query_from_sparql`** function (you can ask the URL of your benchmark by contacting the dev team)- 

```python
out = omni.query_from_sparql(q, URL = "http://imlspenticton.uzh.ch/omni_iris_sparql")

```
All queries typically return a dictionary or a list of dictionaries with fields describing your output. In this case, the function retrieves the following information about the datasets imported by the specified project: 

```
out[0].keys()
> dict_keys(['query', 'full_name', 'short_name', 'keyword', 'creator', 'dateCreated', 'descr', 'originID'])
```


