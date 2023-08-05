
def replace_input(sparql_command, inputs): 
    for i in range(len(inputs)): 
        sparql_command = sparql_command.replace("##INPUT".__add__(str(i)).__add__("##"), inputs[i] )
    return(sparql_command)

def attr(e,n,v): 
    """
    Set attribute to object. Used when creating queries string and to be retrieved by `query_from_sparql`.
    'True' indicates that the query has to be recursive on the output. 
    """
    class tmp(type(e)):
        def attr(self,n,v):
            setattr(self,n,v)
            return self
    return tmp(e).attr(n,v)
def setRecursive():
    return(True)
def setNonRecursive():
    return(False)

