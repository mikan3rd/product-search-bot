import requests

import settings

KEY1 = settings.KEY1

endpoint = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0/detect'

face_url = 'http://idolnextstage.com/wp-content/uploads/2016/08/51.jpg'
test_url = 'http://i.gzn.jp/img/2018/02/08/capsnet/00_m.jpg'


output_list = [
    {'key': 'gender', 'label': '性別'},
    {'key': 'age', 'label': '年齢'},
    {'key': 'smile', 'label': '笑顔'},
    {'key': 'emotion', 'label': '感情'},
    {'key': 'makeup', 'label': '化粧'},
    {'key': 'accessories', 'label': '身につけているもの'},
]

emotion_label = {
    'anger': '怒り',
    'contempt': '軽蔑',
    'disgust': '嫌悪',
    'fear': '恐怖',
    'happiness': '幸せ',
    'neutral': '通常',
    'sadness': '悲しみ',
    'surprise': '驚き',
}

makeup_label = {
    'eyeMakeup': '目',
    'lipMakeup': '唇',
}

accessories_label = {
    'headwear': '帽子',
    'glasses': 'メガネ',
    'mask': 'マスク',
}

convet_data = {
    'facialHair': 'ひげ',
    'glasses': 'メガネ',
    'hair': '髪',
}


def get_face_info(image_url=None, image=None):
    if image_url is None and image is None:
        return '必要な情報が足りません'

    params = {
        'returnFaceId': True,
        'returnFaceLandmarks': False,
        'returnFaceAttributes': 'age,gender,smile,facialHair,glasses,emotion,hair,makeup,accessories',
    }

    if image_url:
        headers = {
            'Ocp-Apim-Subscription-Key': KEY1,
            'Content-Type': 'application/json',
        }
        data = {'url': image_url}
        response = requests.post(
            endpoint,
            headers=headers,
            params=params,
            json=data
        )

    elif image is not None:
        headers = {
            'Ocp-Apim-Subscription-Key': KEY1,
            "Content-Type": "application/octet-stream"
        }
        response = requests.post(
            endpoint,
            headers=headers,
            params=params,
            data=image,
        )

    status = response.status_code
    data = response.json()

    if status != 200:
        error = ''
        if status == 429:
            error = '今月に使用できる回数を超過しました'

        else:
            error = 'エラーが発生しました'

        print(status, data)
        return error

    num = len(data)

    if num == 0:
        return '顔が検知できませんでした'

    if num > 1:
        return '%s人の顔が検出されました' % (num)

    face_info = data[0]['faceAttributes']
    text_list = []

    for option in output_list:
        key = option['key']
        info = face_info.get(key)

        if info is None:
            continue

        output = ''

        if key == 'gender':
            output = '男性' if info == 'male' else '女性'

        elif key == 'age':
            output = '%s歳' % (info)

        elif key == 'smile':
            output = str(round(info * 100, 1)) + '%'

        elif key == 'emotion':
            info_list = sorted(info.items(), key=lambda x: x[1], reverse=True)
            tmp_list = []
            for info in info_list:
                tmp = '%s %s' % (
                    emotion_label[info[0]], round(info[1] * 100, 1))
                tmp_list.append(tmp + '%')
            output = '\n'.join(tmp_list)

        elif key == 'makeup':
            tmp_list = []
            for k, v in info.items():
                tmp = '%s %s' % (makeup_label[k], 'あり' if v else 'なし')
                tmp_list.append(tmp)
            output = '\n'.join(tmp_list)

        elif key == 'accessories':
            if len(info) == 0:
                output = 'なし'

            else:
                tmp_list = [accessories_label[label['type']] for label in info]
                output = ' '.join(tmp_list)

        text_list.append('[%s]\n%s' % (option['label'], output))

    text = '\n\n'.join(text_list)
    print(text)

    return text


if __name__ == "__main__":
    get_face_info()
