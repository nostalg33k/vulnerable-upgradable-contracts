from google.cloud import bigquery
from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm
import signal
import sys
terminate = False

#file to save list of contracts addresses
CONTRACTS_FILE = '../tesst/test'

#dir to save Solidity source code
CONTRACTS_DIR = '../tesst/'

NB_SOURCE = 0
NB_DELEGATE = 0

def get_contracts_from_bigQuery():
    """
    Fetch contracts from BigQuery Ethereum dataset.

    """
    global CONTRACTS_FILE
    client = bigquery.Client()

    # SQL query to request all contracts from 01/01/2019 to 31/05/2019.
    new_contracts_query = 'SELECT address  ' \
                          'FROM `bigquery-public-data.crypto_ethereum.contracts` ' \
                          'WHERE block_timestamp >= "{}-{}-{} 00:00:00" ' \
                          'AND block_timestamp < "{}-{}-{} 00:00:00" ' \
                          'AND bytecode != "0x" ' \
                          'ORDER BY block_timestamp'.format('2019','01','01','2019','05','31')

    query_job = client.query(new_contracts_query)

    # Waits for job to complete.
    results = query_job.result()

    print('Contracts fetched')

    # List contracts in CONTRACTS_FILE separated by newline character
    with open(CONTRACTS_FILE,'w') as file:
        for row in results:
            file.write(row.address + '\n')


def get_delegate_code(address):
    """
    Save Solidity contract source code if available at Etherscan and using delegatecall in CONTRACTS_DIR.

    :param address: address of the contract
    """
    global NB_SOURCE
    global NB_DELEGATE


    url = "https://etherscan.io/address/%s#code" % address

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('Error: {}  Contract: {}  Url: {}\n'.format(e, address, url))
        return

    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    # No source code
    if soup.find(id="editor") == None:
        return

    name = soup.find("span", class_="h6 font-weight-bold mb-0").contents[0]
    code = str(soup.find(id="editor")).replace('<pre class="js-sourcecopyarea editor" id="editor" style="margin-top: 5px;">', '').replace('</pre>','')

    # No source code
    if len(code) <= 0:
        return
    NB_SOURCE += 1

    # No delegatecall in code
    if 'delegatecall' in code:
        NB_DELEGATE +=1
    else:
        return

    # Fetch contract name if available
    fname = name if len(name) > 0 else address

    #Manage duplicate names
    if os.path.isfile(CONTRACTS_DIR+fname+'.sol'):
        i=0;
        while os.path.isfile(CONTRACTS_DIR+fname+str(i)+'.sol'):
            i+=1
        fname += str(i)
    fname += ".sol"

    # Save .sol file
    with open(CONTRACTS_DIR + fname, 'w') as of:
        of.write('//Contract address: '+ address+'\n'+ code)
        of.flush()

def sigint_handler(signum, frame):
    global terminate
    terminate = True


if __name__ == '__main__':
    contracts_count = 0
    signal.signal(signal.SIGINT,sigint_handler)

    #get_contracts_from_bigQuery()

    with open(CONTRACTS_FILE,'r') as file:
        lines = file.readlines()
        for line in tqdm(lines):
            get_delegate_code(line.rstrip())
            contracts_count += 1

            if terminate:
                print('\nStopped collecting at line: {}'.format(line))
                print('Number of contracts processed: {}\nNumber of contracts with source code: {}\nNumber of contracts with delegatecall: {}'.format(contracts_count,NB_SOURCE,NB_DELEGATE))
                sys.exit(0)

    print('\nNumber of contracts processed: {}\nNumber of contracts with source code: {}\nNumber of contracts with delegatecall: {}'.format(contracts_count, NB_SOURCE, NB_DELEGATE))