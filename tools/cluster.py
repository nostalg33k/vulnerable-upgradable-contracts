from tqdm import tqdm
import json
from json import JSONDecoder, JSONDecodeError
import os
import sys


import distance
import ssdeep
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
import matplotlib.pyplot as plt



class contract:


    address_list = []
    name_list = []
    hash_list = []
    contract_list = []

    def __init__(self, jsonObj):
        self.address = jsonObj['address']

        self.name = jsonObj['name']
        self.bytecode = jsonObj['bytecode']
        self.hash = ssdeep.hash(self.bytecode)
        contract.contract_list.append(self)
        contract.address_list.append(self.address)
        contract.name_list.append(self.name)
        contract.hash_list.append(self.sh)
