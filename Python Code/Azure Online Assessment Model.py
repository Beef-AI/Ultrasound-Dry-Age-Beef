from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os
import csv

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"

prediction_key = "335d2cad11f14b1d9502056347c27323"
project_id = "0a2a0106-5cf4-4e19-a44c-2cab16c83314"
publish_iteration_name = "Iteration1"


def appendcsv(csv_item):
    csv_list = []
    try:
        with open('predict.csv', newline='') as fp:
            rows = csv.reader(fp)
            for row in rows:
                csv_list.append(row)
    except:
        pass
    csv_list.append(csv_item)
    with open('predict.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(csv_list)

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

path = 'source'
header_created = False
header_names = []
dir_list = os.listdir(path)
dir_list_sort = sorted(dir_list, key=lambda n: int('.'.join(n.split('.')[0:-1]).split('_')[-1]))

for name in dir_list_sort:
    while True:
        try:
            with open(os.path.join(path, name), 'rb') as image_contents:
                results = predictor.classify_image(project_id, publish_iteration_name, image_contents.read())
            print(name)

            if not header_created:
                header_created = True
                item = ['name']
                for prediction in results.predictions:
                    item.append(prediction.tag_name)
                    header_names.append(prediction.tag_name)
                appendcsv(item)
                current_predictions = {pred.tag_name: '{:.2f}'.format(pred.probability * 100) for pred in results.predictions}
                sorted_predictions = [current_predictions.get(tag, '0.00') for tag in header_names]
                appendcsv([name] + sorted_predictions)
            else:
                current_predictions = {pred.tag_name: '{:.2f}'.format(pred.probability * 100) for pred in results.predictions}
                sorted_predictions = [current_predictions.get(tag, '0.00') for tag in header_names]
                item = [name] + sorted_predictions
                appendcsv(item)
            break
        except:
            print("retry")
            continue