import clarifai
from clarifai.rest import ClarifaiApp

app = ClarifaiApp(api_key='ab7a257992dd4a39a6cce25e706ae0bc')


model=app.models.get("general-v1.3")

list=[]
tags= model.predict_by_url(url="https://si.wsj.net/public/resources/images/BN-QD448_WORKFA_GR_20161006132343.jpg")
print tags['outputs'][0]['data']['concepts'][1]['name']
#for temp in tags['outputs'][0]['data']['concepts']:
    #print '1. ', temp  , '\n'
    #if temp['value']>0.95:
     #   print temp['name']
      #  list.append(temp['name'])

print list
