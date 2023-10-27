import transformers
import pandas as pd

from transformers import pipeline
model = "distilbert-base-uncased-finetuned-sst-2-english"

sentiment_pipeline = pipeline("sentiment-analysis",model=model)
df = pd.read_csv('yt_vid_comments2.csv')

test = df[:100]

author_text_dict = {author: [text] for author, text in zip(test['author'], test['text'])} 

for key in author_text_dict:
    if len(author_text_dict[key][0]) < 2000:      
        output = sentiment_pipeline(author_text_dict[key])
        label = output[0]['label']
        score = output[0]['score']
        author_text_dict[key].extend([label,score])

result = pd.DataFrame.from_dict(author_text_dict,orient='index').reset_index()
result = result.rename(columns={'index':'author',0:'comment',1:'label',2:'score'})

# for item in list(result[result.label == 'POSITIVE'].comment):
#     print(item)
#     print("-------------------------------------------------------")

print(len(result[result.label == "POSITIVE"]) / len(result[result.label == "NEGATIVE"]))
