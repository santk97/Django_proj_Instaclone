import clarifai
from clarifai.rest import ClarifaiApp

app = ClarifaiApp(api_key='ab7a257992dd4a39a6cce25e706ae0bc')


model=app.models.get("general-v1.3")


print model.predict_by_url(url="http://www.gettyimages.com/gi-resources/images/Embed/new/embed2.jpg")