# BayesNetCreacion
This library has the objective of building Bayesian networks and making probabilistic inference over them. Also, adding some other additional features that could serve the developers that make use of this library.  
This library has zero dependencies to assure it is futureproof, easier to debug, to contribute to and use.  
For the most part this library works over classes like BayesNetCreacion and Node, this was chosen so that in a way it could facilitate the usage of the OOP paradigm.


For further inquiries you about the usage of the library you can consult [Usage](#usage) section of this repo or the [testing](/BayesNetCreacion/testing.py) python file to see the Burglar Alarm System example being used.

### Features

- Created without using any dependencies/libraries.
- Can create Bayesian Networks, represented as a dictionary.
- Calculation of probabilistic inference given the created Bayesian Network.
- Can check if network is fully defined or not.
- Has the capability of returning a compact representation of the network as a string.
- Can return the network's factors as a dictionary.
- Is able to return the numeration of the network given evidence and a query.

### Prerequisites
- Python 3.10.^

### Install
```bash
pip install BayesNetCreacion
```

### Usage
```python
from BayesNetCreacion import BayesNetCreacion, Node #Import the library

examplenode = Node('E') #Create a Node object
example2node = Node('E2') #Create another Node object
example2node.set_parents([str(examplenode)]) #Set node as parent

bnc = BayesNetCreacion() #Instantiate the Bayes Network class

#Add both nodes into the network
bnc.add_node(examplenode)
bnc.add_node(example2node) 

#Add the probability values of each node 
bnc.add_prob({
    ('E', True): 0.001,
    ('E', False): 0.999,
    ('E2', True, 'E', True): 0.25,
    ('E2', True, 'E', False): 0.9,
    ('E2', False, 'E', True): 0.75,
    ('E2', False, 'E', False): 0.1
})

#Features:

#Get dictionary with network
bn = bnc.get_network()

#Probabilistic inference
evidence = {'E': True}
query = 'E2'

result = bnc.probabilistic_inference(query, evidence) #Calculate the inference
print(result) #Profit?

#Compact
WIP

#Factors
print(bnc.get_factors())

#Definition Check
WIP

#Enumeration
evidence = {'E': False}
query = 'E2'
result = bnc.pre_enum(query, evidence) #Calculate numeration
print(result)

```

## Author
👤 Andrés de la Roca
 - <a href = "https://www.linkedin.com/in/andr%C3%A8s-de-la-roca-pineda-10a40319b/">Linkedin</a> 
 - <a href="https://github.com/andresdlRoca">Github</a>  
