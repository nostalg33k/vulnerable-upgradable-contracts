import json
import re

import distance
import numpy as np
import pydeep
import tqdm
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AffinityPropagation

NOT_WHITESPACE = re.compile(r'[^\s]')


def decode_stacked(document, pos=0, decoder=json.JSONDecoder()):
    while True:
        match = NOT_WHITESPACE.search(document, pos)
        if not match:
            return
        pos = match.start()

        try:
            obj, pos = decoder.raw_decode(document, pos)
        except json.JSONDecodeError:
            raise
        yield obj


class contract:


    address_list = []
    name_list = []
    hash_list = []
    contract_list = []

    def __init__(self, jsonObj):
        self.address = jsonObj['address']
        self.name = jsonObj['contract_name']
        self.bytecode = jsonObj['bytecode']
        self.hash = pydeep.hash_buf(self.bytecode)
        contract.contract_list.append(self)
        contract.address_list.append(self.address)
        contract.name_list.append(self.name)
        contract.hash_list.append(self.hash)


def create_contracts(contracts_file):
    with open(contracts_file, "r") as myfile:
        contracts = myfile.read()

    for obj in tqdm.tqdm(decode_stacked(contracts)):
        new_c = contract(obj)

    print("Contract bytecode hashes computed.")


# Compute similarity matrix with mean of 3 distances
def compute_similarity(X):
    jaccard_matrix = pdist(X, lambda x, y: distance.jaccard(x[0], y[0]))
    np.savetxt("../data/jaccard_matrix.csv", np.asarray(squareform(jaccard_matrix)), delimiter=",")

    sorensen_matrix = pdist(X, lambda x, y: distance.sorensen(x[0], y[0]))
    np.savetxt("../data/sorensen_matrix.csv", np.asarray(squareform(sorensen_matrix)), delimiter=",")

    # normalized, so that the results can be meaningfully compared
    # method=1 means the shortest alignment between the sequences is taken as factor
    levenshtein_matrix = pdist(X, lambda x, y: distance.nlevenshtein(x[0], y[0], method=1))
    np.savetxt("../data/levenshtein_matrix.csv", np.asarray(squareform(levenshtein_matrix)), delimiter=",")

    mean_matrix = 1 - np.mean(np.array([jaccard_matrix, sorensen_matrix, levenshtein_matrix]), axis=0)
    np.savetxt("../data/similarity_matrix.csv", np.asarray(mean_matrix), delimiter=",")

    print("Similarity matrix computed.")
    return mean_matrix


def clusterize(X):
    af = AffinityPropagation(affinity="precomputed", max_iter=2000, convergence_iter=200, damping=0.9)
    af.fit(similarity_matrix)
    cluster_centers_indices = af.cluster_centers_indices_
    num_of_clusters = len(cluster_centers_indices)
    labels = af.labels_

    print('Number of clusters: %d' % num_of_clusters)

    # output file as csv: contract name - contract address - ssdeep hash - cluster
    output = []
    for i in range(len(labels)):
        c = [contract.name_list[i], contract.address_list[i], contract.hash_list[i], labels[i]]
        output.append(c)

    np.savetxt("../data/contracts_clustering.csv", output, delimiter="],", fmt='%s')
    return output, cluster_centers_indices, labels


if __name__ == '__main__':
    create_contracts('../data/contracts_list')

    X = np.array(contract.hash_list).reshape(-1, 1)

    similarity_matrix = compute_similarity(X)

    output, indices, labels = clusterize(similarity_matrix)
