import os
import sys
from pathlib import Path
import json
import torch
import torch.nn.functional as F
from miditok import REMI

sys.path.append("src/continuous_generator")
from src.continuous_generator.LSTMwithAtt import LSTMwithAtt

'''
jsonからロード
'''

#モデルとプロンプトの選択
model_path = "resources/models/lstmwithatt_best.pt"
tokenizer_path = "resources/tokenizers/piano1_tokens/tokenizer.json"
prompt_path = "inputs/output.mid"
generation_length = 500

#ベクトル表示の非短縮設定
torch.set_printoptions(edgeitems=torch.inf)

def generate_midi(model_path, tokenizer_path, prompt_path, generation_length):
    #device setting
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    #tokenizerの読み込み
    tokenizer = REMI(params=Path(tokenizer_path))

    # mmodelの選択
    hidden_size = 200
    model = LSTMwithAtt(tokenizer, hidden_size)

    model.load_state_dict(torch.load(Path(model_path), map_location=device))
    model = model.to(device)

    #promptの読み込み
    prompt_path = (Path(prompt_path))

    #promptのトークン化
    input_ids = torch.tensor([tokenizer(prompt_path)]).to(device)
    print("prompt tokenized", input_ids.shape, input_ids)


    model.eval()

    gen_token = []

    with torch.no_grad():
        x = model.input_emb(input_ids)
        ox, (hnx, cnx) = model.lstm1(x)
        hnx, cnx = hnx[:,0,:], cnx[:,0,:]
        wid = input_ids[0][0]
        
        sl = 0
        while True:
            wids = torch.LongTensor([wid]).to(device)
            y = model.answer_emb(wids)
            
            oy, (hnx, cnx) = model.lstm2(y, (hnx, cnx))
            oy = oy.unsqueeze(1)
            ox1 = ox.permute(0,2,1)
            sim = torch.bmm(oy,ox1)
            bs, yws, xws = sim.shape
            sim2 = sim.reshape(bs*yws,xws)
            alpha = F.softmax(sim2,dim=1).reshape(bs, yws, xws)
            ct = torch.bmm(alpha,ox)
            oy1 = torch.cat([ct,oy],dim=2)
            oy2 = model.Wc(oy1)
            oy3 = model.W(oy2)
            wid = torch.argmax(oy3[0]).item()
            gen_token.append(wid)
            #if (wid == esid):
                #break
            if (sl == generation_length):
                break
            sl += 1
        print(gen_token)

    generated = tokenizer.decode(gen_token)
    print("Generated MIDI Tokens:", generated)

    #genarated_midi = "resources/generated/" + model_name + "_from_" + prompt_name + ".mid"
    genarated_midi = "resources/generated/generated.mid"

    generated.dump_midi(genarated_midi)

if __name__ == "__main__":
    generate_midi(model_path, tokenizer_path, prompt_path, generation_length)
