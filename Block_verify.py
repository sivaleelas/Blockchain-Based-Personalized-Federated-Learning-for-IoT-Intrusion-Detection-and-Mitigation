import random
import hashlib

# Define a Validator class
class Validator:
    def __init__(self, name, stake):
        """
        Initialize a Validator with a name, stake (amount staked), and reputation.
        Stake represents how much cryptocurrency the validator has locked up.
        Reputation starts at 1 and can be adjusted based on validator performance.
        """
        self.name = name
        self.stake = stake
        self.reputation = 1  # Reputation for fair validator selection
        self.is_active = True  # Validator's active status

    def slash(self, amount):
        """
        Slash the validator's stake as a penalty for malicious or negligent behavior.
        """
        self.stake -= amount
        if self.stake < 0:
            self.stake = 0  # Prevent negative stake
        print(f"{self.name} has been slashed by {amount}. New stake: {self.stake}")


# Define a Block to store weights and verification status
class Block:
    def __init__(self, block_height, model_weights, validator, previous_hash=''):
        """
        Create a new block in the blockchain. A block contains:
        - The current block height (position in the chain).
        - The model weights (in this case, simplified as a string or hash).
        - The validator who proposed the block.
        - The previous block's hash to link the chain.
        """
        self.block_height = block_height
        self.model_weights = model_weights  # Store model weights
        self.validator = validator  # Validator that created this block
        self.previous_hash = previous_hash  # Hash of the previous block
        self.block_hash = self.compute_hash()  # Compute current block hash

    def compute_hash(self):
        """
        Compute a SHA-256 hash of the block's content to ensure integrity.
        """
        block_content = str(self.block_height) + str(self.model_weights) + self.validator.name + self.previous_hash
        return hashlib.sha256(block_content.encode()).hexdigest()


# Define a Blockchain class to manage validators and store weights in the blockchain
class Blockchain:
    def __init__(self):
        """
        Initialize the Blockchain with an empty list of validators, an empty chain, and block height 0.
        """
        self.validators = []  # List to hold all validators in the network
        self.chain = []  # Blockchain to store model weights
        self.block_height = 0  # Represents the height of the blockchain (number of blocks)

    def add_validator(self, validator):
        """
        Add a new validator to the list of validators.
        """
        self.validators.append(validator)

    def select_validator(self):
        """
        Select a validator to propose a new block based on stake and reputation.
        Uses a weighted random selection based on stake and reputation.
        """
        total_stake = sum([validator.stake for validator in self.validators])
        
        # Cap the stake to avoid wealth bias and weight with reputation
        capped_stakes = [min(validator.stake, 100) for validator in self.validators]
        weighted_stakes = [capped_stake * validator.reputation for validator, capped_stake in zip(self.validators, capped_stakes)]
        
        # Normalize the weighted stakes to probabilities
        selection_probs = [weight / sum(weighted_stakes) for weight in weighted_stakes]
        
        # Randomly select a validator based on their weighted probability
        selected_validator = random.choices(self.validators, weights=selection_probs, k=1)[0]
        return selected_validator

    def verify_weights(self, model_weights):
        """
        Simulate verification of model weights by validators.
        Validators check the integrity of the weights before accepting the block.
        (In a real implementation, this would involve hash checks, cryptographic signatures, etc.)
        """
        valid = random.choice([True, False])  # Randomly simulate verification (replace with real checks)
        return valid

    def add_block(self, model_weights):
        """
        Add a block to the blockchain. If validators verify the weights, the block is added.
        """
        selected_validator = self.select_validator()
        print(f"Validator {selected_validator.name} selected to propose a block.")

        # Validators verify the model weights
        if self.verify_weights(model_weights):
            print(f"Model weights verified by validator {selected_validator.name}. Block added.")
            # Create the new block
            previous_hash = self.chain[-1].block_hash if self.chain else '0'
            new_block = Block(self.block_height, model_weights, selected_validator, previous_hash)
            self.chain.append(new_block)  # Add block to the blockchain
            self.block_height += 1
        else:
            print(f"Validator {selected_validator.name} failed to verify the weights. Block rejected.")

    def get_block_by_height(self, block_height):
        """
        Fetch a block from the blockchain based on its height.
        This is used to retrieve verified model weights.
        """
        for block in self.chain:
            if block.block_height == block_height:
                return block
        return None


# # Sample usage: Simulate saving and verifying model weights in the blockchain

# # Define some validators with stakes
# v1 = Validator("Validator 1", 50)
# v2 = Validator("Validator 2", 200)
# v3 = Validator("Validator 3", 150)

# # Initialize the blockchain
# blockchain = Blockchain()

# # Add validators to the network
# blockchain.add_validator(v1)
# blockchain.add_validator(v2)
# blockchain.add_validator(v3)

# # Simulate saving and verifying model weights
# model_weights = "WeightsHash123"  # Simulated model weights (use hash or actual weights in a real scenario)

# # Add blocks containing the model weights
# blockchain.add_block(model_weights)  # Block 1
# blockchain.add_block(model_weights)  # Block 2

# # Retrieve and verify the block containing the weights from the blockchain
# block = blockchain.get_block_by_height(1)
# if block:
#     print(f"Block {block.block_height} found: Weights: {block.model_weights}, Validator: {block.validator.name}")
# else:
#     print("Block not found.")


# import numpy as np
# import hashlib
# import random
# import time

# # Define the Validator class for MPoSC
# class Validator:
#     def __init__(self, name, stake):
#         self.name = name
#         self.stake = stake  # Stake held by the validator

#     def validate(self):
#         # Randomized validation logic based on stake (higher stake -> higher chance of selection)
#         return random.random() < self.stake / (self.stake + random.randint(1, 1000))


# # Define the Block class
# class Block:
#     def __init__(self, model_weights, previous_hash, validator):
#         self.timestamp = time.time()
#         self.model_weights = model_weights  # Store model weights in the block
#         self.previous_hash = previous_hash  # Hash of the previous block
#         self.validator = validator  # Validator who verified the block
#         self.hash = self.calculate_hash()  # Calculate current block's hash

#     def calculate_hash(self):
#         # Calculate the hash for the block (based on model weights, timestamp, and previous hash)
#         block_data = str(self.model_weights) + str(self.timestamp) + self.previous_hash
#         return hashlib.sha256(block_data.encode()).hexdigest()


# # Define the Blockchain class
# class Blockchain:
#     def __init__(self):
#         self.chain = [self.create_genesis_block()]
#         self.validators = []
#         self.block_height = 1  # Track height of the blockchain

#     def create_genesis_block(self):
#         # Create the genesis (first) block in the blockchain
#         return Block(model_weights="Genesis Block", previous_hash="0", validator=None)

#     def add_validator(self, validator):
#         # Add a validator to the network
#         self.validators.append(validator)

#     def select_validator(self):
#         # Select a validator using Modified Proof of Stake Consensus (MPoSC)
#         # Higher stake validators have higher chances to be selected
#         eligible_validators = [v for v in self.validators if v.validate()]
#         if eligible_validators:
#             return random.choice(eligible_validators)  # Randomly select one from eligible validators
#         return None

#     def add_block(self, model_weights):
#         # Add a new block with model weights to the blockchain
#         validator = self.select_validator()  # Choose validator using MPoSC
#         if validator:
#             previous_hash = self.chain[-1].hash
#             new_block = Block(model_weights=model_weights, previous_hash=previous_hash, validator=validator)
#             self.chain.append(new_block)
#             self.block_height += 1
#             print(f"Block added by {validator.name} at height {self.block_height}")
#         else:
#             print("No eligible validator found, block not added.")

#     def get_block_by_height(self, height):
#         # Get a block by its height
#         if height <= self.block_height and height > 0:
#             return self.chain[height]
#         else:
#             return None

