import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split 
from gan_glru import *
from Block_verify import *
from keras.models import load_model
from Existing import *


"DDoS Botnet"
df=pd.read_csv("Datasets/DDoSdata.csv")
normal_data = df[df['attack'] ==0]
normal_data_expanded = pd.concat([normal_data] *3000, ignore_index=True)
combined_df = pd.concat([df, normal_data_expanded], ignore_index=True)
labels=combined_df['attack']
data=combined_df.drop(['attack'],axis=1)
stng_data_list=list(data.columns)
for i in stng_data_list:
    if data[i].dtype == 'object':  # Apply encoding only to object (string) columns
        data[i] = data[i].astype(str)  # Convert all values to strings
        data[i] = LabelEncoder().fit_transform(data[i])
    # print(f"Processed column: {i}")
data=np.array(data)
labels=np.array(labels)
x_train,x_test,y_train,y_test=train_test_split(data,labels,test_size=0.2)

x_train_=np.array_split(x_train, 10, axis=0)
y_train_=np.array_split(y_train, 10, axis=0)

comms_rounds =1
blockchain = Blockchain()
v1 = Validator("Validator 1", 50)
v2 = Validator("Validator 2", 200)
v3 = Validator("Validator 3", 150)
blockchain.add_validator(v1)
blockchain.add_validator(v2)
blockchain.add_validator(v3)



# Communication Rounds
for round_ in range(comms_rounds):
    weights = []  # List to store verified weights for this round

    # Iterate over data partitions
    for ind, (x, y) in enumerate(zip(x_train_, y_train_)):
        # Reshape the data
        x_ = x.reshape(x.shape[0], 1, x.shape[-1])
        print("*" * 30)
        print(f"DATA-------{ind}")
        print("*" * 30)

        # Squeeze labels
        y = y.squeeze()

        # Create and train the local model
        local_model = GAN_GLRU(x_,y)  # Placeholder model, replace with your actual GAN_GLRU
        local_model.fit(x_, y, epochs=1, batch_size=32, verbose=1, validation_split=0.2)

        # Get the model weights after training
        model_weights = local_model.get_weights()

        # Add model weights as a block to the blockchain
        blockchain.add_block(model_weights)

        # Verifying the block using MPoSC
        print(f"Verifying model weights from blockchain for model {ind}...")
        block = blockchain.get_block_by_height(blockchain.block_height - 1)  # Get the last block

        if block:
            # If the block is verified, append the weights
            print(f"Model weights from {ind} verified successfully by {block.validator.name}.")
            weights.append(block.model_weights)  # Store the verified weights
        else:
            print(f"Failed to verify weights for model {ind}.")
       
    if len(weights) > 0:
        new_weights = [np.zeros_like(weight) for weight in weights[0]]  # Initialize list of zeros
        
        for weight in weights:
            for i in range(len(new_weights)):
                new_weights[i] += weight[i]
        
        # Averaging weights by dividing by the number of models
        new_weights = [weight / len(weights) for weight in new_weights]
    x_train=x_train.reshape(x_train.shape[0],1,x_train.shape[-1])
    global_model=GAN_GLRU(x_train,y_train)
    global_model.set_weights(new_weights)
        
    global_model.save("Models/dataset1/Proposed_model.h5")
    