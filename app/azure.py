import json
import requests
import os

BASE_URL = "https://westus2.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"
TEXT_KEY = os.getenv('AZURE_TEXT_KEY')


def sentiment(data):
    """ 情感分析 """
    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': TEXT_KEY,
    }

    body = json.dumps(data)

    try:
        request = requests.post(BASE_URL, data=body, headers=headers)
        data = request.json()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def azure(id, text):
    data = {
        "documents": [
            {
                "language": "en",
                "id": id,
                "text": text
            }
        ]
    }
    result = sentiment(data)
    print('===== Collection of documents to analyze.')
    print(data)
    print('===== sentiment result')
    print(result)

    return result
