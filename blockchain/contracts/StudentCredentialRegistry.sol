// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title StudentCredentialRegistry
 * @dev Tamper-evident academic & skill credential registry on Ethereum EVM.
 * Only cryptographic hashes and non-sensitive identifiers are stored on-chain.
 */
contract StudentCredentialRegistry {
    address public owner;

    enum CredentialType {
        SkillAssessment,
        CourseCompletion,
        Achievement,
        CareerReadiness
    }

    struct CredentialRecord {
        string credentialId;
        address studentAddress;
        bytes32 credentialHash; // SHA-256 hash of credential JSON
        CredentialType credType;
        uint256 issuedTimestamp;
        address issuer;
        bool isValid;
    }

    // Mapping from credentialId => CredentialRecord
    mapping(string => CredentialRecord) private credentials;
    // Array of all registered credential IDs
    string[] private credentialIds;

    event CredentialIssued(
        string indexed credentialId,
        address indexed studentAddress,
        bytes32 credentialHash,
        CredentialType credType,
        uint256 issuedTimestamp,
        address issuer
    );

    event CredentialRevoked(
        string indexed credentialId,
        address indexed revokedBy,
        uint256 timestamp
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "Only registry owner can execute this");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function issueCredential(
        string memory _credentialId,
        address _studentAddress,
        bytes32 _credentialHash,
        CredentialType _credType
    ) external onlyOwner {
        require(credentials[_credentialId].issuedTimestamp == 0, "Credential ID already exists");
        require(_credentialHash != bytes32(0), "Invalid credential hash");

        credentials[_credentialId] = CredentialRecord({
            credentialId: _credentialId,
            studentAddress: _studentAddress,
            credentialHash: _credentialHash,
            credType: _credType,
            issuedTimestamp: block.timestamp,
            issuer: msg.sender,
            isValid: true
        });

        credentialIds.push(_credentialId);

        emit CredentialIssued(
            _credentialId,
            _studentAddress,
            _credentialHash,
            _credType,
            block.timestamp,
            msg.sender
        );
    }

    function verifyCredential(
        string memory _credentialId,
        bytes32 _expectedHash
    ) external view returns (bool isValid, bool hashMatches, uint256 timestamp, address issuer) {
        CredentialRecord memory record = credentials[_credentialId];
        if (record.issuedTimestamp == 0 || !record.isValid) {
            return (false, false, 0, address(0));
        }

        bool matches = (record.credentialHash == _expectedHash);
        return (record.isValid, matches, record.issuedTimestamp, record.issuer);
    }

    function revokeCredential(string memory _credentialId) external onlyOwner {
        require(credentials[_credentialId].issuedTimestamp > 0, "Credential not found");
        credentials[_credentialId].isValid = false;
        emit CredentialRevoked(_credentialId, msg.sender, block.timestamp);
    }

    function getTotalCredentials() external view returns (uint256) {
        return credentialIds.length;
    }
}
