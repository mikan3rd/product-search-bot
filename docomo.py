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

    # data = {
    #     'recognitionId': '03c30e90-51dc-11e8-b8a1-06d990afaf44',
    #     'candidates': [
    #         {
    #             'score': 48157.178385416664,
    #             'itemId': 'food_0000133783',
    #             'category': 'food',
    #             'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/815nWbAHZoL._SL1500_.jpg',
    #             'detail': {
    #                 'brand': 'どん兵衛',
    #                 'itemName': 'どん兵衛きつねうどん',
    #                 'releaseDate': '2007/04/09',
    #                 'maker': '日清食品',
    #                 'dimension': '14.2 x 14.2 x 7.7 cm'
    #             },
    #             'sites': [
    #                 {
    #                     'url': 'http://www.amazon.co.jp/gp/product/B000JOWAQ4',
    #                     'title': 'Amazon | どん兵衛きつねうどん | どん兵衛 | うどん 通販',
    #                     'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/815nWbAHZoL._SL1500_.jpg'
    #                 }
    #             ]
    #         },
    #         {
    #             'score': 7488.125,
    #             'itemId': 'food_0000258173',
    #             'category': 'food',
    #             'imageUrl': 'http://ecx.images-amazon.com/images/I/41Z%2BfW7PF1L.jpg',
    #             'detail': {
    #                 'quantity': '12',
    #                 'brand': '日清食品',
    #                 'itemName': '日清食品 日清のどん兵衛 肉うどん 1箱12食',
    #                 'releaseDate': '2011/02/18', 'maker': '日清食品'},
    #             'sites': [{
    #                 'url': 'http://www.amazon.co.jp/gp/product/B001I50YNE',
    #                 'title': 'Amazon.co.jp: 日清食品日清のどん兵衛 肉うどん 1箱12食: 食品・飲料・お酒 通販',
    #                 'imageUrl': 'http://ecx.images-amazon.com/images/I/41Z%2BfW7PF1L.jpg'}]},
    #         {
    #             'score': 6769.880208333333, 'itemId': 'food_0001512920', 'category': 'food',
    #             'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61cjjf7JKHL._SX342_.jpg',
    #             'detail': {
    #                 'weight': '1.6 Kg', 'brand': 'どん兵衛', 'itemName': '日清のどん兵衛 きつねうどん 食べ比べ東 96g',
    #                 'releaseDate': '2017/04/23', 'maker': '日清食品', 'dimension': '44 x 29.5 x 15.5 cm'
    #             }, 'sites': [{
    #                 'url': 'http://www.amazon.co.jp/gp/product/B071Y6J1LB',
    #                 'title': 'Amazon | 日清のどん兵衛 きつねうどん 食べ比べ東 96g | どん兵衛 | 食品・飲料・お酒 通販',
    #                 'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61cjjf7JKHL._SX342_.jpg'}]},
    #         {
    #             'score': 3996.5026041666665, 'itemId': 'food_0000467596', 'category': 'food',
    #             'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81D4sH9-9QL._SL1500_.jpg',
    #             'detail': {
    #                 'weight': '109 g', 'preservation': '常温', 'brand': 'どん兵衛',
    #                 'itemName': '日清 どん兵衛カレーうどん 91g', 'releaseDate': '2012/02/28',
    #                 'maker': '日清食品', 'dimension': '14.4 x 14.4 x 7.5 cm'},
    #             'sites': [{
    #                 'url': 'http://www.amazon.co.jp/gp/product/B003VQHJ6S',
    #                 'title': 'Amazon | 日清 どん兵衛カレーうどん 91g | どん兵衛 | ラーメン 通販',
    #                 'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81D4sH9-9QL._SL1500_.jpg'}]},
    #         {
    #             'score': 3704.9440104166665, 'itemId': 'food_0000070218',
    #             'category': 'food', 'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51jLrVJ-iFL._SX475_.jpg',
    #             'detail': {
    #                 'weight': '2.3 Kg', 'brand': 'どん兵衛', 'itemName': '日清 どん兵衛 特盛きつねうどん東 131g×12個',
    #                 'releaseDate': '2011/06/07', 'maker': '日清食品', 'dimension': '16.8 x 51.2 x 34.4 cm'
    #             }, 'sites': [{'url': 'http://www.amazon.co.jp/gp/product/B0054NT7Z2',
    #                           'title': 'Amazon | 日清 どん兵衛 特盛きつねうどん東 131g×12個 | どん兵衛 | 食品・飲料・お酒 通販',
    #                           'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51jLrVJ-iFL._SX475_.jpg'}
    #                          ]}]
    # }

    candidates = data.get('candidates')

    if not candidates:
        return '商品が見つかりませんでした'

    result = [
        {
            "thumbnailImageUrl": content['imageUrl'],
            "title": content['detail']['itemName'],
            "text": "{maker}： {brand}\n発売日： {releaseDate}"
            .format(**content['detail']),
            "actions": [{
                "type": "uri",
                "label": "商品ページを見る",
                "uri": content['sites'][0]['url']
            }]
        }
        for content in candidates
    ]

    return result


if __name__ == "__main__":
    search_product()
