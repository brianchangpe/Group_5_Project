# Streamlit Application 

###### DOA VOTING PAGE ########

# Imports
from asyncore import poll
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


################################################################################
# Polls Information:

#if analysis, if nr of polls gr than 0 than display the dropdown

st.title("Number of Active Polls: ")
st.write(contract.functions.NumberOfPolls().call())

for i in range(1, contract.functions.NumberOfPolls().call()+1):
    print(i)


# for i in range(1, numberofpolls+1)
# loop (i) 1 thru numberofpolls 
    # call poll (i)
    # display that poll information

#if st.button("Add Voter"):
#    poll_id = st.input("Add Poll Id")
#    voter_address = """

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



#at the end of the code we can have the results on a bar chart for each candidate and each poll!

###st.bar_chart({"data": [1, 5, 2, 6, 2, 1]}) #voting results on bar chart


################################################################################
# Streamlit Sidebar Code

#st.sidebar.markdown("## Voting Information", polls_list)"""

##########################################

# Creating a select box to chose between different polls:
#polls = st.sidebar.selectbox('Select a Poll', )"""




#Work done by Prakruti

# Create a subheader for your application
st.subheader("You can only cast one vote")

# Adding selections
library = st.radio(
    "Please select below",
    ("Yes", "No")
)

if st.button("Display selection"):
    st.write(library)
