import requests

import settings

CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
API_KEY = settings.API_KEY

endpoint = 'https://api.apigw.smt.docomo.ne.jp/imageRecognition/v1/recognize'


def search_product(image=None):
    if image is None:
        return '必要な情報が足りません'

    params = {
        'APIKEY': API_KEY,
        'recog': 'product-all',
        'numOfCandidates': 5,
    }

    headers = {"Content-Type": "application/octet-stream"}

    response = requests.post(
        endpoint,
        headers=headers,
        params=params,
        data=image,
    )

    status = response.status_code
    data = response.json()

    if status != 200 and status != 204:
        error = 'エラーが発生しました'
        print(status, data)
        return error

    num = len(data)

    if num == 0:
        return '商品が見つかりませんでした'

    print(data)

    return 'test'


if __name__ == "__main__":
    search_product()
