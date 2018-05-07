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

    print(data)

    if status != 200 and status != 204:

        if status == 403:
            error = '今月に使用できる回数を超過しました'

        else:
            error = 'エラーが発生しました'

        print(status, data)
        return error

    candidates = data.get('candidates')

    if not candidates:
        return '商品が見つかりませんでした'

    results = []
    for content in candidates:
        content['detail']['maker'] = \
            content['detail'].get('maker') or  \
            content['detail'].get('publisher', '')

        content['detail']['brand'] = \
            content['detail'].get('brand') or  \
            content['detail'].get('author', '')

        imageUrl = 'https://i.vimeocdn.com/video/443809727.jpg?mw=700&mh=394'

        if content['imageUrl'].startswith('https'):
            imageUrl = content['imageUrl']

        result = {
            "thumbnail_image_url": imageUrl,
            "title": content['detail']['itemName'],
            "text": "{maker}： {brand}\n発売日： {releaseDate}"
            .format(**content['detail']),
            "actions": {
                "label": "商品ページを見る",
                "uri": content['sites'][0]['url']
            }
        }
        results.append(result)

    print(results)

    return results


if __name__ == "__main__":
    search_product()
