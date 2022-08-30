import pandas as pd
from sentence_transformers import SentenceTransformer, util
import re
import torch

def cleanData(documents):
    # #한글 및 띄어쓰기만 남기고 제거
    document = re.sub('[^ 가-힣]+',"",str(documents))
             
    #특수문자 제거
    # document = re.sub('[★◆●▶♥🐱♻△♡冠☝🦺●◆@#$-=+,#/\:^$.@*\"※&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》;:↑→‘’]',"",document)  
    
    return document
# jhgan/ko-sroberta-multitask
model = SentenceTransformer('jhgan/ko-sroberta-multitask')

df = pd.read_csv('./testing_csv_raw.csv')[['number','string']]

# 새로운 문장 입력
query = '피부가 뒤집어졌어요 개싫어요 비추천합니다'#input("문장입력")

new_embeddings = model.encode(query, convert_to_tensor=True)

#불러온 데이터의 text 리스트화
original_text = [i.strip() for i in df['string'].apply(lambda x: cleanData(x)) if len(i)>0]

old_embeddings =  model.encode(original_text, convert_to_tensor=True)

#유사도 점수
cosine_scores = util.pytorch_cos_sim(new_embeddings, old_embeddings)

# 코사인 유사도 순으로 `top_k` 개 문장 추출
top_results = torch.topk(cosine_scores, k=30)

print(f"입력 문장: {query}")
print(f"\n<입력 문장과 유사한 {30} 개의 문장>\n")

print('top_results[0]',top_results[0])
print('top_results[1]',top_results[1])

for i, (score, idx) in enumerate(zip(top_results[0][0], top_results[1][0])):
    print(f"{i+1}: {original_text[idx]} {'(유사도: {:.4f})'.format(score)}\n")