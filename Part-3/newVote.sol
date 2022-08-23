pragma solidity ^0.5.0;


contract ComVote {//is ERC20{

    struct Poll{
        string name;
        string uri;
        uint voteCount;
        uint voteSupport;   
        uint pollId; 
    }

    address payable public chairperson;
    mapping(uint => Poll) public polls;
    //mapping(uint => address[] ) pollVoters; 
    mapping (uint => mapping(address => bool)) pollVoters;
    mapping(uint => address[] ) pollCommittee;
    uint public NumberOfPolls = 0;

    constructor()public{
        chairperson=msg.sender;
    }

    modifier isCommittee(uint pollId){
        //Poll storage poll = polls[pollId];
        bool found = false;
        for (uint i=0; i< pollCommittee[pollId].length; i++){
            if (msg.sender == pollCommittee[pollId][i]){
                found = true;
            }
        }
        require(found, "You are not in that polls committee");
        _;
    }

    modifier isVoter(uint pollId){
        //Poll storage poll = polls[pollId];
        require(pollVoters[pollId][msg.sender], "You are not in that polls committee");
        _;
    }
    
    function addVoter(uint pollId, address newVoter) public isCommittee(pollId) {
        pollVoters[pollId][newVoter] = true;
    }

    function vote(uint pollId, bool support) public isVoter(pollId){
        polls[pollId].voteCount += 1;
        if (support){
            polls[pollId].voteSupport +=1;
        }
        pollVoters[pollId][msg.sender] = false;
    }

    function hasMajority(uint pollId) public view returns(bool){
        return ( (polls[pollId].voteCount / 2) < polls[pollId].voteSupport );
    }

    function createPoll(string memory _name, string memory _uri) public returns(uint256) {
        require (msg.sender == chairperson);
        NumberOfPolls += 1;
        polls[NumberOfPolls] = Poll(_name, _uri, 0, 0, NumberOfPolls);
        return NumberOfPolls;
    }


}