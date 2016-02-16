# participation
the python package to express data from participation instances as RDF linked data for the semantic web.

## core features
  - database schemas for proper triplification.
  - routines for publishing RDF linked data from diverse participation instances (portals/mechanisms).
  - compliance to the participation ontology and the percolation package for harnessing open linked social data.

## install with
    $ pip install participation
or

    $ python setup.py participation

For greater control of customization (and debugging), clone the repo and install with pip with -e:

    $ git clone https://github.com/ttm/participation.git
    $ pip install -e <path_to_repo>
This install method is especially useful when reloading modified module in subsequent runs of participation.

Participation is integrated to the participation ontology and the percolation package
to enable anthropological physics experiments and social harnessing:
- https://github.com/ttm/percolation

## coding conventions
A function name has a verb if it changes state of initialized objects, if it only "returns something", it is has no verb in name.

Classes, functions and variables are writen in CamelCase, headlessCamelCase and lowercase, respectively.
Underline is used only in variable names where the words in variable name make something unreadable (usually because the resulting name is big).

The code is the documentation. Code should be very readable to avoid writing unnecessary documentation and duplicating routine representations. This adds up to using docstrings to give context to the objects or omitting the docstrings.

Tasks might have c("some status message") which are printed with time interval in seconds between P.check calls.
These messages are turned of by setting P.QUIET=True or calling P.silence() which just sets P.QUIET=True

The usual variables in scripts are: P for percolation, NS for P.rdf.NS for namespace, a for NS.rdf.type, c for P.check, Pa for participation, r for rdflib, x for networkx, k for nltk... Variables have larger names to better describe the routine.

Every feature should be related to at least one legacy/ outline.

Routines should be oriented towards making RDF data from participatory instances/portals/mechanisms data.

### package structure
Data not in RDF are kept in the data/ directory.
Credentials for mysql, postgresql and mongodb connections should be left in G.PARTICIPATIONDIR+accesses.py.
Each platform/protocol has an umbrella module in which are modules for accessing current data in platforms
and expressing them as RDF.
This package relies heavily in the percolation package to assist rendering of RDF data.

#### the modules are:
bootstrap.py for starting system with basic variables and routines

aa/\* 
- access.py to access to aa data from mysql, mongodb irc logs and ORe
- render.py for expressing aa shouts and sessions as rdf 

participabr/\* 
- access.py to access participabr data from postgresql (and any other API)
- render.py for expressing participabr data as rdf (posts, comments, participation tracks, steps, friendships)

cidadedemocratica/\* 
- access.py to access cidade democratica data from mysql
- render.py for expressing cidade democratica data as rdf (posts, observatories, tags, cities, etc)

legacy.py for legacy routines and enrichment triples
utils.py for small functionalities that fit nowhere else

## usage example
```python
import participation as Pa

Pa.publishLegacy() # publish as rdf all data in data/

```

## further information
Analyses and media rendering of the published RDF data is dealt with by the percolation package: https://github.com/ttm/percolation

Social package for expressing data from Facebook, Twitter and IRC: https://github.com/ttm/social

Gmane package for expressing data from public email lists in Gmane archive: https://github.com/ttm/gmane

Participation package for expressing data from participatory platforms such as AA, Particpabr and Cidade Democrática:
https://github.com/ttm/participation
