import hashlib
import json
from datetime import datetime


def generate_hash(record):
    """Generate SHA-256 hash for an academic record."""
    record_string = json.dumps(
        record, sort_keys=True
    )
    return hashlib.sha256(
        record_string.encode()
    ).hexdigest()


def create_block(record, previous_hash="0"):
    """Create a new academic record block."""
    block = {
        "timestamp": datetime.now().isoformat(),
        "record": record,
        "previous_hash": previous_hash
    }

    block["hash"] = generate_hash(block)

    return block


def verify_block(block):
    """Verify whether the block data is unchanged."""
    original_hash = block.get("hash")

    data = {
        "timestamp": block["timestamp"],
        "record": block["record"],
        "previous_hash": block["previous_hash"]
    }

    return original_hash == generate_hash(data)


def create_blockchain(records):
    """Create a blockchain from academic records."""
    blockchain = []
    previous_hash = "0"

    for record in records:
        block = create_block(record, previous_hash)
        blockchain.append(block)
        previous_hash = block["hash"]

    return blockchain


def verify_blockchain(blockchain):
    """Verify every block and its connection to the previous block."""

    for index, block in enumerate(blockchain):

        # Verify the block's own hash
        if not verify_block(block):
            return False

        # Verify the connection to the previous block
        if index == 0:
            if block["previous_hash"] != "0":
                return False
        else:
            expected_hash = blockchain[index - 1]["hash"]

            if block["previous_hash"] != expected_hash:
                return False

    return True
