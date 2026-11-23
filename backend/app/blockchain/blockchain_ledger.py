import hashlib
import json
import os
import time
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class Block:
    def __init__(
        self,
        index: int,
        timestamp: float,
        transactions: List[Dict[str, Any]],
        previous_hash: str,
        nonce: int = 0
    ):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

class BlockchainLedger:
    def __init__(self, ledger_file: str = "blockchain_ledger.json"):
        self.ledger_file = ledger_file
        self.chain: List[Block] = []
        self.difficulty = 2 # Lightweight difficulty for instant local verification
        self.load_or_initialize()

    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            timestamp=1700000000.0,
            transactions=[{
                "type": "GENESIS",
                "issuer": "0x0000000000000000000000000000000000000000",
                "credential_id": "GENESIS-BLOCK",
                "credential_hash": hashlib.sha256(b"EduCareer-AI-Genesis").hexdigest(),
                "timestamp": 1700000000.0
            }],
            previous_hash="0" * 64,
            nonce=0
        )
        self.chain.append(genesis_block)
        self.save_chain()

    def load_or_initialize(self):
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, "r") as f:
                    data = json.load(f)
                    self.chain = []
                    for b in data:
                        block = Block(
                            index=b["index"],
                            timestamp=b["timestamp"],
                            transactions=b["transactions"],
                            previous_hash=b["previous_hash"],
                            nonce=b["nonce"]
                        )
                        block.hash = b["hash"]
                        self.chain.append(block)
                return
            except Exception:
                pass
        self.create_genesis_block()

    def save_chain(self):
        with open(self.ledger_file, "w") as f:
            json.dump([b.to_dict() for b in self.chain], f, indent=2)

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_credential(
        self,
        credential_id: str,
        student_id: int,
        title: str,
        credential_type: str,
        metadata: Dict[str, Any],
        issuer: str = "0x71C...EDUGUIDE_ROOT_CA"
    ) -> Dict[str, Any]:
        """Creates cryptographic hash of credential, mines block, and appends to ledger."""
        # Cryptographic hash of the credential payload
        cred_payload = {
            "credential_id": credential_id,
            "student_id": student_id,
            "title": title,
            "credential_type": credential_type,
            "metadata": metadata,
            "issuer": issuer
        }
        cred_hash = hashlib.sha256(json.dumps(cred_payload, sort_keys=True).encode()).hexdigest()
        
        tx_data = {
            "tx_id": f"0x{hashlib.sha256((credential_id + str(time.time())).encode()).hexdigest()}",
            "credential_id": credential_id,
            "student_id": student_id,
            "title": title,
            "credential_type": credential_type,
            "credential_hash": cred_hash,
            "issuer": issuer,
            "timestamp": time.time()
        }

        # Create new block
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.time(),
            transactions=[tx_data],
            previous_hash=last_block.hash,
            nonce=0
        )

        # Simple proof of work
        prefix = "0" * self.difficulty
        while not new_block.hash.startswith(prefix):
            new_block.nonce += 1
            new_block.hash = new_block.compute_hash()

        self.chain.append(new_block)
        self.save_chain()

        return {
            "block_number": new_block.index,
            "block_hash": new_block.hash,
            "tx_hash": tx_data["tx_id"],
            "credential_hash": cred_hash,
            "issuer": issuer,
            "timestamp": new_block.timestamp
        }

    def verify_credential(self, credential_id: str, expected_hash: Optional[str] = None) -> Dict[str, Any]:
        """Validates blockchain integrity and confirms credential authenticity."""
        # 1. Check ledger integrity
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]
            if current.previous_hash != prev.hash:
                return {
                    "is_valid": False,
                    "tamper_detected": True,
                    "details": f"Blockchain corrupted at Block #{current.index}: previous hash mismatch!"
                }
            if current.hash != current.compute_hash():
                return {
                    "is_valid": False,
                    "tamper_detected": True,
                    "details": f"Block #{current.index} hash was tampered!"
                }

        # 2. Find credential in chain
        for block in self.chain:
            for tx in block.transactions:
                if tx.get("credential_id") == credential_id:
                    tx_hash = tx.get("credential_hash")
                    if expected_hash and tx_hash != expected_hash:
                        return {
                            "is_valid": False,
                            "tamper_detected": True,
                            "details": "Certificate hash does not match the immutable ledger record! Tampering detected."
                        }
                    return {
                        "is_valid": True,
                        "tamper_detected": False,
                        "credential_id": credential_id,
                        "title": tx.get("title"),
                        "credential_type": tx.get("credential_type"),
                        "credential_hash": tx_hash,
                        "tx_hash": tx.get("tx_id"),
                        "block_number": block.index,
                        "issuer": tx.get("issuer"),
                        "timestamp": tx.get("timestamp"),
                        "details": "Cryptographically verified on immutable blockchain ledger."
                    }

        return {
            "is_valid": False,
            "tamper_detected": False,
            "details": f"Credential ID '{credential_id}' not found in the blockchain registry."
        }

blockchain_ledger = BlockchainLedger()
