# lab-2-ia

## Bayesian Network Python Implementation

### Author: Roberto Rios

Laboratorio 2 - semestre 1

Inteligencia Artificial

### Version: Alpha 0.0.2

To install, run on terminal:

```console
pip install rrbayesnet
```

Start importing the package:

```console
from rrbayesnet import BayesianNetwork
```

Create your net

```console

bn = BayesianNetwork({
    "Burglary": ["Alarm"],
    "Earthquake":["Alarm"],
    "Alarm": ["JohnCalls", "MaryCalls"]
    })

```

Then, you might need to fill the nodes with its probabilities

```console

# it will automatically add the complements

bn.setParentNodeProb("Burglary", 0.002)
bn.setParentNodeProb("Earthquake", 0.001)

bn.setDepNodeProb("Alarm", [0.94, 0.95, 0.69, 0.999])
bn.setDepNodeProb("JhonCalls", [0.91, 0.05])
bn.setDepNodeProb("MaryCalls", [0.75, 0.02])

```

Then, you can run the services

```console

bn.getCompact()
bn.describe()
bn.factors()
bn.inference()

```

### Services

the principal services are:

[x] BayesianNetwork.describe() -> checks if a probability is missing, and returns the nodes with the missings ones
[x] BayesianNetwork.factors() -> returns every probability and node in the structure (True or false, and conditionals)
[x] BayesianNetwork.getCompact() -> returns a string with the full expression for the Probability of every node given its parents

### Tests

The tests and structure were design by following the next example:

![alt text](https://www.researchgate.net/profile/Joost-Vennekens/publication/265933295/figure/fig2/AS:638057757806592@1529136232237/Bayesian-network-for-alarm-system.png)

### References and usefull links

https://www.javatpoint.com/bayesian-belief-network-in-artificial-intelligence

https://pypi.org/project/rrbayesnet/
