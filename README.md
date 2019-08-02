# Upgradeable smart contracts measurements
<table>
    <tr>
        <td><img src="images/sefcom.png?raw=true" width="256" title="Sefcom"></td>
        <td><img src="images/1280px-Grenoble_INP_-_Esisar_(logo).svg.png?raw=true" width="256" title="Esisar"></td>
    </tr>
</table>

  
<br />


Project realized during a 5-months SEFCOM apprenticeship to validate my engineering degree. 

## Motivation
In Ethereum, smart contracts are immutable by nature. Yet, it is possible to work around this limitation to create upgradeable smart contracts. 
This project aims to study the proportion of upgradeable smart contracts in the blockchain and analyze them.

## Content
This repo the dataset that was used for the analysis, the python codes for the scraper to get the data from etherscan and the clustering algorithm. It also contains a python code to find Solidity function selector collisions.  


## Requirements
* Python version 3.7 was used.

###_Native_
- json
- re

###_3rd party_
- beautifulsoup4==4.8.0
- Distance==0.1.3
- numpy==1.17.0
- pycryptodomex==3.8.2
- requests==2.21.0
- scikit-learn==0.21.3
- scipy==1.3.0
- tqdm==4.32.2

## File structure
- **data** - 2 files containing stacked json objects representing smart contracts and identified as using the Proxy pattern for upgradability. This is a subset of the BigQuery Ethereum dataset (https://bigquery.cloud.google.com/dataset/bigquery-public-data:ethereum_blockchain).
    - **2019_contracts_list** - contains 990 upgradeable contracts _created between 01/01/2019 and 31/05/2019_.
    - **contracts_list** - contains 2462 upgradeable contracts randomly selected in the BigQuery dataset _minus the one created in 2019_.
    
    Attributes of the json objects are:
    - **contract_nameX** - name of the contract as fetched on Etherscan + random number
    - **address** - address of the contract
    - **upgrade_hash** - optional. function selector of the upgrade function(s)
    - **transactions** - optional. transactions emitted to upgrade the contract
    - **tr_count** - optional. number of transactions
    - **bytecode** - bytecode of the contract as fetched on Etherscan
    
    - **distance_matrix.csv** - csv file of the distance matrix computed and used in the clustering algorithm

- **tools**: python scripts
    - **cluster.py**
    - **selector-collision-finder.py**
    
- **rapport_fr**: my LaTeX internship school report


