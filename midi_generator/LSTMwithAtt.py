import torch
import torch.nn as nn
import torch.nn.functional as F

class LSTMwithAtt(nn.Module):
    def __init__(self, tokenizer, lstm_hidden):
        super(LSTMwithAtt, self).__init__()
        input_size = tokenizer.vocab_size
        self.input_emb = nn.Embedding(input_size, lstm_hidden, padding_idx=0)
        self.answer_emb = nn.Embedding(input_size, lstm_hidden, padding_idx=0)
        self.lstm1 = nn.LSTM(lstm_hidden, lstm_hidden, num_layers=2, batch_first=True)
        self.lstm2 = nn.LSTM(lstm_hidden, lstm_hidden, num_layers=2, batch_first=True)
        self.Wc = nn.Linear(2*lstm_hidden, lstm_hidden)
        self.W = nn.Linear(lstm_hidden, input_size)

    def forward(self, token, answer_token):
        x = self.input_emb(token)
        ox, (hnx, cnx) = self.lstm1(x)
        y = self.answer_emb(answer_token)
        oy, (hny, cny) = self.lstm2(y, (hnx, cnx))
        ox1 = ox.permute(0, 2, 1)
        sim = torch.bmm(oy, ox1)
        bs, yws, xws = sim.shape
        sim2 = sim.reshape(bs*yws, xws)
        alpha = F.softmax(sim2, dim=1).reshape(bs, yws, xws)
        ct = torch.bmm(alpha, ox)
        oy1 = torch.cat([oy, ct], dim=2)
        oy2 = self.Wc(oy1)

        return self.W(oy2)
