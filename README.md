# Upgradeable smart contracts measurements

<br />


Project realized during a 5-months SEFCOM apprenticeship to validate my engineering degree. 

##Motivation
In Ethereum, smart contracts are immutable by nature. Yet, it is possible to work around this limitation to create upgradeable smart contracts. 
This project aims to study the proportion of upgradeable smart contracts in the blockchain and analyze them.

## Content
This repo the dataset that was used for the analysis, the python codes for the scraper to get the data from etherscan and the clustering algorithm. It also contains a python code to find Solidity function selector collisions.  


## Requirements
* Python version 3.7 was used.

## Files
- **data** - contains 2 files, 2019_contracts_list and contracts_list. Both contains stacked json objects representing smart contracts identified as upgradable by using the Proxy pattern. Attributes are:
    - contract_nameX - name of the contract as fetched on Etherscan + random number
    - address - address of the contract
    - upgrade_hash - optional. function selector of the upgrade function(s)
    - transactions - optional. transactions emitted to upgrade the contract
    - tr_count - optional. number of transactions
    - bytecode - bytecode of the contract as fetched on Etherscan
- **rapport_fr**: my LaTeX internship school report
- **tools**: contains the python codes

