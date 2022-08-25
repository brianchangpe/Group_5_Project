pragma solidity ^0.5.0;


contract ComVote {//is ERC20{

    struct Poll{
        string name;
        string uri;
        uint voteCount;
        uint voteSupport;   
        uint pollId; 
        uint pollDeadlineInHours;
    }

    address payable public chairperson;
    mapping(uint => Poll) public polls;
    //mapping(uint => address[] ) pollVoters; 
    mapping (uint => mapping(address => bool)) public pollVoters;
    mapping(uint => mapping(address => bool)) public pollCommittee;
    uint public NumberOfPolls = 0;

    constructor()public{
        chairperson=msg.sender;
    }

    modifier isCommittee(uint pollId){
        //Poll storage poll = polls[pollId];
        require(pollCommittee[pollId][msg.sender], "You are not in that polls committee");
        _;
    }

    modifier isVoter(uint pollId){
        //Poll storage poll = polls[pollId];
        require(pollVoters[pollId][msg.sender], "You are not in that polls committee");
        _;
    }
    
    modifier isActive (uint pollId){
        require(polls[pollId].pollDeadlineInHours > now, "This poll has ended.");
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
        return ( (polls[pollId].voteCount) < polls[pollId].voteSupport * 2);
    }

    function createPoll(string memory _name, string memory _uri, uint pollDeadlineInHours) public returns(uint256) {
        require (msg.sender == chairperson);
        NumberOfPolls += 1;
        uint t =  pollDeadlineInHours * 1 hours;
        polls[NumberOfPolls] = Poll(_name, _uri, 0, 0, NumberOfPolls, t);
        pollCommittee[NumberOfPolls][chairperson] = true;
        return NumberOfPolls;
        
    }
}