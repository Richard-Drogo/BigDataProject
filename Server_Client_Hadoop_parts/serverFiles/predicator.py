import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from pytorch_pretrained_bert import BertTokenizer, BertConfig
from pytorch_pretrained_bert import BertAdam, BertForSequenceClassification
from transformers import WEIGHTS_NAME, CONFIG_NAME
import pandas as pd
import io
import numpy as np
import os
import torch.nn.functional as F 


# class used for prediction with BertForSequenceClassification pre-trained model
class Predicator:
    # the different jobs that are predicted
    __predict_job = [
        "pastor","model","yoga_teacher","teacher",
        "personal_trainer","painter","journalist","interior_designer",
        "surgeon","accountant","dj","physician","comedian",
        "software_engineer", "nurse","poet","dentist","chiropractor",
        "filmmaker","professor","photographer","rapper","psychologist",
        "paralegal","architect","composer","attorney","dietitian"
    ]
    # instance of BertForSequenceClassification made
    # can take several seconds bcs of the initialisation of bert model
    def __init__(self,output_dir="./models/"):
        # get device
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        n_gpu = torch.cuda.device_count()
        # get model from weight 
        self.__model = BertForSequenceClassification.from_pretrained(output_dir,num_labels=28)
        # create tokenizer
        self.__tokenizer = BertTokenizer.from_pretrained(output_dir)
        self.__model.eval()

    # use this function to predict from an array with the summaries
    # rturn dataframe with description and prediction  for each jobs 
    def prediction(self,inputArray):
        # tokenize
        inputs = self.__create_inputs_ids(inputArray)
        # create mask
        b_input_mask = self.__create_attention_masks(inputs)
        # create dataloader
        dataloader = self.__create_dataloader(inputs,[0 for i in inputs],b_input_mask,1)
        # get description
        values_DF = self.__model_prediction(dataloader)
        # create dataframe
        final_res = pd.DataFrame(np.array(inputArray),columns = ["Summary"])
        return final_res.join(values_DF)

    # tokenize from an array of srting
    def __create_inputs_ids(self,x_set,MAX_LEN = 128):
        x_spe_set = ['[CLS] '+x+' [SEP]' for x in x_set]
        x_tokenized = [self.__tokenizer.tokenize(x) for x in x_spe_set]
        input_ids = [self.__tokenizer.convert_tokens_to_ids(x) for x in x_tokenized]
        input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")
        return input_ids

    # create mask
    def __create_attention_masks(self,input_ids):
        attention_masks = []
        # Create a mask of 1s for each token followed by 0s for padding
        for seq in input_ids:
            seq_mask = [float(i>0) for i in seq]
            attention_masks.append(seq_mask)
        return attention_masks
    
    # create dataloader
    def __create_dataloader(self,inputs,labels,masks,batch_size = 32):
        tsr_inputs = torch.tensor(inputs)
        tsr_lables = torch.tensor(labels)
        tsr_masks = torch.tensor(masks)
        data = TensorDataset(tsr_inputs, tsr_masks, tsr_lables)
        sampler = RandomSampler(data)
        dataloader = DataLoader(data, sampler=sampler, batch_size=batch_size)
        return dataloader

    # predict
    def __model_prediction(self,dataloader):
        res = []
        for batch in dataloader:
            # Unpack the inputs from our dataloader
            b_input_ids, b_input_mask, b_labels = batch
            b_input_ids = torch.tensor(b_input_ids).to(torch.int64)
            # to gpu
            b_input_mask.to(self.__device)
            b_input_ids.to(self.__device)
            b_labels.to(self.__device)
            with torch.no_grad():
                # Forward pass, calculate logit predictions
                logits = self.__model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask)
            # normalize 
            norm = [F.softmax(logit).tolist() for logit in logits]
            res.append(norm)
        
        toDf = []
        for r_batch in res :
            for r in r_batch :
                toDf.append(r)

        df = pd.DataFrame(toDf[::-1], columns=self.__predict_job)
        return df


# exemple
#output_dir = "D:\models/"
#inputs = ["Since she was 10 years old she has become a model. Later, she started her acting career in 1999 as a little actress as well.Moon Geun Young once dating a handsome actor Kim Bum.According to the news, their love story started from the drama Goddes of Fire, Jung Yi in 2013. After dating about 7 months, they reportedly broke up.",
#            "Playing with computer since childhood, Audric get into a scientfic enginneer schools from which he will be diplomed this years."]
#pred = Predicator(output_dir=output_dir)
#print(pred.prediction(inputs))

