import random
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import os



class Users(): 
    def receive_response(self,response):
        print(response)
        
class IOT(Users):
    def __init__(self):
        self.n_sensors=100
    def send_response(self,response):
        self.receive_response(response)
    def respond_to_Users(self,response):
        self.send_response(response)
      
class Network(IOT):
    def __init__(self):
        
        
        self.number_of_data=100
        self.Attack_status=np.load('Features/dataset3/Labels.npy',allow_pickle=True)
        print("Blockchain driven Personalized Federated Learning Model for intrusion detection and mitigation")
        print()
        self.model = load_model('Models/dataset3/Proposed_model.h5') 
        self.total=[]
        
    
    def FL(self,user_data_, label,data):
        user_data=np.asarray(user_data_)
        user_data = user_data.reshape(1,1,user_data.shape[-1])
        self.atk_pred =self.model.predict(user_data)
        self.pred = np.argmax(self.atk_pred)
        result=self.Attack_status[self.pred]
        self.find = label
        
        
        
        if self.find==0:
            print("Predicted   ")
            print()
            print(" --------  Normal --------")
            print()
            user_data_1 = {}
            for i in data.keys():
                user_data_1[i] = [data.get(i)]  # Wrap values in a list
            
            data_ = pd.DataFrame(user_data_1)
            
            file_path = 'Features/dataset3/Server.csv'
            if not os.path.exists(file_path):
                # If file doesn't exist, create it and write the header
                data_.to_csv(file_path, mode='w', index=False, header=True)
            else:
                # If file exists, append without the header
                data_.to_csv(file_path, mode='a', index=False, header=False)
            print("Added to Server")

           
        else:
            print("Predicted   ")
            print()
            print(" -------- Attack -------- ")
            print()
            print("Attack detected. User data not saved to the server.")
    def fetch_Users(self):
        print("Collecting Users Data")
        df=pd.read_csv("Datasets/Train_Test_Network__.csv")
        stng_data_list=list(df.columns)
        for i in stng_data_list:
            if df[i].dtype == 'object':  # Apply encoding only to object (string) columns
                df[i] = df[i].astype(str)  # Convert all values to strings
                df[i] = LabelEncoder().fit_transform(df[i])
        
        return df
        
        
    def run(self):
        data = self.fetch_Users()
        self.wrong_pred=[]
        count = 0
        while count < self.number_of_data:
            a = random.randint(0, len(data))
            Users = data.iloc[a, :]
            data_=Users.drop(['label'])
            label = Users["label"]
            print("Actual  :",int(label))
            print('Detecting the  attack using the detection model')
            self.FL(data_, label,Users)
            print()
            count += 1      
if __name__ == "__main__" :
    
    net = Network()        
    net.run() 

   
    
    
    

    
    

    

    

    
        
          

