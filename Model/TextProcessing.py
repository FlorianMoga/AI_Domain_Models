import json
import requests

URL = 'https://api-leodev.gep.com/leo-portal-domainmodel-api/api/v1/DomainModel/UpdateEntity'

KEYWORDS = {"date": ["date"],
            "invoice_number": ["invoice-no.", "invoice no.", "invoice no", "invoice-num.", "invoice-number",
                               "invoice number"],
            "money": ["$", '£', '€', 'RON', "amount", "total"],
            "address": ["str", 'street'],
            "recipient": ["recipient"]
            }

FIELD = {
    "name": "",
    "type": {
        "name": "",
        "actualType": "",
        "id": "",
        "isPrimitiveType": True
    }
}

WHOLE = {
    "entity": {"draftId": "798b8201-756d-4da4-8f4d-53b5323572fa",
               "subtypeId": "f479f415-a423-4df4-90ac-cd255fe1814c",
               "model": {
                   "modelName": "",
                   "entityDescription": "",
                   "isRootEntity": False,
                   "isAvailableForRest": False,
                   "fields": []
               }
               }
}

stringId = "3454534543"
stringName = "Plain Text"
stringActualType = "string"

floatId = "1644566262"
floatName = "Decimal Number"
floatActualType = "decimal"


class TextProcessing:
    def __init__(self, text):
        self.text = text
        self.associatedClusters = None
        self.ID = None
        self.set_clusters_attr(self.text)

        self.entities = []
        self.fields = []
        self.fieldTypes = []
        self.values = []

    def set_clusters_attr(self, invoice_text):
        segments = []
        segments_words = []
        asscociatedClusters = []

        for text in invoice_text:
            segments.append(text.strip('\n'))

        for segment in segments:
            segments_words.append(segment.split("\n"))

        for cluster_text in segments:
            categories = []
            for key, values in KEYWORDS.items():
                for value in values:
                    if value in cluster_text.lower():
                        categories.append(key)

            if len(set(categories)) > 0:
                asscociatedClusters.append([list(set(categories)), cluster_text])

        self.associatedClusters = asscociatedClusters

    def createJSON(self, jsonFile):

        with open(jsonFile) as json_file:
            data = json.load(json_file)

        for cluster in self.associatedClusters:
            cluster[1] = cluster[1].split('\n')
            cluster[1] = list(filter(''.__ne__, cluster[1]))
            if cluster[0] == ['address']:
                if cluster[1][0].lower() == 'billed to':
                    data['reciever']['companyName'] = cluster[1][1]
                    data['reciever']['streetAddress'] = cluster[1][2][5:]
                    data['reciever']['city'] = cluster[1][3].split(',')[0].strip(' ')
                    data['reciever']['state'] = cluster[1][3].split(',')[1].strip(' ')
                    data['reciever']['zip'] = cluster[1][4]
                    data['reciever']['country'] = cluster[1][5]
                    data['reciever']['phone'] = cluster[1][6]
                else:
                    data['sender']['companyName'] = cluster[1][0]
                    data['sender']['streetAddress'] = cluster[1][1][5:]
                    data['sender']['city'] = cluster[1][2].split(',')[0].strip(' ')
                    data['sender']['state'] = cluster[1][2].split(',')[1].strip(' ')
                    data['sender']['zip'] = cluster[1][3]
                    data['sender']['country'] = cluster[1][4]
                    data['sender']['phone'] = cluster[1][5]
            elif cluster[0] == ['money']:
                words = cluster[1][0].split()
                data['amount']['currency'] = words[-1][0]
                data['amount']['depositDue'] = float(words[-1][1:].replace(',', ''))
            elif cluster[0] == ['date']:
                data['date']['dueDate'] = cluster[1][1]
            else:
                info = cluster[1][1]
                info = info.split()
                print(info)

                date = " ".join(map(lambda x: x, info[:-2]))
                data['date']['dateIssued'] = date
                data['invoiceNum'] = info[-2]
                data['amount']['amountDue'] = float(info[-1][1:].replace(',', ''))

        with open("JSON/" + data['invoiceNum'] + ".json", "w") as outfile:
            json.dump(data, outfile, indent=4)

        return data['invoiceNum'] + ".json"

    def set_dictionary(self, some_dict):


        for key, val in some_dict.items():
            field, fieldType, value = [], [], []
            if type(val) is dict:
                for k, v in val.items():
                    if k == 'amountDue' or k == 'depositDue':
                        valType = 'float'
                    else:
                        valType = 'string'
                    field.append(k)
                    fieldType.append(valType)
                    value.append(v)
            else:
                field.append(key)
                fieldType.append('string')
                value.append(val)

            entity = key
            self.entities.append(entity)
            self.fields.append(field)
            self.fieldTypes.append(fieldType)
            self.values.append(value)

    def createRequestGEP(self, token):
        for e, entity in enumerate(self.entities):
            wholeCustom = dict(WHOLE)
            wholeCustom['entity']['model']['modelName'] = entity
            fieldList = []
            for it in range(len(self.fields[e])):
                fieldCustom = dict(FIELD)
                fieldCustom['name'] = self.fields[e][it]
                if self.fieldTypes[e][it] == 'string':
                    Id, name, actualType = stringId, stringName, stringActualType
                else:
                    Id, name, actualType = floatId, floatName, floatActualType
                fieldCustom['type']['name'], fieldCustom['type']['actualType'], fieldCustom['type'][
                    'id'] = name, actualType, Id
                fieldList.append(fieldCustom)
            wholeCustom['entity']['model']['fields'] = fieldList
            print(wholeCustom)
            ##
            result = requests.post(URL, json=wholeCustom,
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(token),
                                            'ocp-apim-subscription-key': '018ca54b6f5743bfa732ad309adf9e8f'})
            print(result.text)
