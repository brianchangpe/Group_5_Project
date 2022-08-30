# Streamlit Application 

###### DOA VOTING PAGE ########

# Imports
from asyncore import poll
from audioop import add
from tkinter import N
from tokenize import Name
from unicodedata import name
import streamlit as st
from web3 import Web3
from streamlit_lottie import st_lottie
from PIL import Image
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv
import os
import json
load_dotenv()

# Defining and connecting the Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

print(os.getenv("WEB3_PROVIDER_URI"))

# Creating the title of our application using markdown syntax and Streamlit

st.markdown("# DAO VOTING PAGE !")

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

voting = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_MtN0BG.json")
construction = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_5eofrmfd.json")
voted = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_rfL75m.json")
results = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_keoed4f6.json")
wip = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_k8naqfew.json")
cip = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_bsatc9vq.json")

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st_lottie(voting, height = 220, key="voting gif")
    with right_column:
        st_lottie(construction, height = 220, key="construction gif")
    st.write("---")

################################################################################
# Load_Contract Function

#Trying to load the contract abi but !!!failing!!!

@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contract/newVote_abi.json')) as f:
        vote_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    print(contract_address)
    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=vote_abi
    )

    return contract


# Load the contract
contract = load_contract()

address = w3.eth.accounts[0] # maybe use selected address in metamask or drop down
st.write("Address of the Ethereum Smart Contract:", address)


################################################################################
# Polls Information:
poll_name = st.sidebar.text_input("Create a Voting Poll")
poll_uri = "www.google.com"
poll_hours = 24


if st.sidebar.button("Create Poll"):
    st.title("Create Poll!")
    tx_hash = contract.functions.createPoll(
        poll_name,
        poll_uri,
        poll_hours
    ).transact({'from':address, "gas":1000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Poll Created, this is the receipt of that transaction:")
    st.write(dict(receipt))

#if analysis, if nr of polls gr than 0 than display the dropdown

st.subheader("Number of Active Polls: ")
st.write(contract.functions.NumberOfPolls().call())

pollId = st.selectbox("Select Poll:", range(1, contract.functions.NumberOfPolls().call()+1))

address = st.sidebar.selectbox("Select the address", w3.eth.accounts)

st.write(contract.functions.polls(pollId).call())


# for i in range(1, numberofpolls+1)
# loop (i) 1 thru numberofpolls 
    # call poll (i)
    # display that poll information

#poll_id = st.sidebar.text_input("Add Poll Id")
#newVoter = st.sidebar.text_input("Voters Address")

if st.sidebar.button("Add Voter"):
    st.sidebar.title("Adding a new Voter")

    tx_hash = contract.functions.addVotertoAll(
    address, #line92 instead of newVoter
    ).transact({'from':w3.eth.accounts[0], "gas":1000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Voter added, this is the receipt of that transaction:")
    st.write(dict(receipt))

################################################################################
# Streamlit Sidebar Code

#st.sidebar.markdown("## Voting Information", polls_list)"""

##########################################

# Creating a select box to chose between different polls:
#polls = st.sidebar.selectbox('Select a Poll', )"""

# Create a subheader for your application

with st.container():
    st_lottie(voted, height = 220, key="voted gif")
st.markdown("You can only cast one vote")
# Adding selections
library = st.radio(
    "Please select below",
    ("Yes", "No")
)

if st.button("Vote"):
    support = True
    if library == "Yes":
        support = True
    elif library == "No":
        support = False
        
    tx_hash = contract.functions.vote(
        pollId,
        support,
    ).transact({'from':address, "gas":1000000})

    # we can also print the receipt of the transaction:
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    st.write(f"This Address {address} Voted, and this is the receipt of the Vote counted:")
    st.write(dict(receipt))


with st.container():
    st_lottie(results, height = 220, key="poll results gif")
st.markdown("Voting Results:")

votesVolt = {} # here I am creating a dictionary vault for the votes count

for Poll in range(1, contract.functions.NumberOfPolls().call()+1):
    pollCount = contract.functions.polls(Poll).call()
    #st.write(pollCount)
    votesVolt[pollCount[4]] = pollCount[3]

st.write(votesVolt)


#at the end of the code we can have the results on a bar chart for each candidate and each poll!

st.bar_chart(
    {"data": votesVolt}) #voting results on bar chart

st.write("---")
with st.container():
    left_column, right_column = st.columns(2)
with left_column:
    st_lottie(wip, height = 220, key="work in progress gif")
with right_column:
    st_lottie(cip, height = 220, key="construction in progress gif")

st.write("---")

