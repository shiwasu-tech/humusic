import torch
import torch.nn as nn
import torch.nn.functional as F

class LSTMwithAttention(nn.Module):
    def __init__(self):
        super(LSTMwithAttention, self).__init__()
    
    