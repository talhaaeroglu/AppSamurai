import requests
import json


def json_cost_calculator(obj):
    return_list = []

    def json_flattener(v, flattened_key=''):
        if isinstance(v, dict):
            for k, v2 in v.items():
                if k == "items":
                    p2 = "{}{}".format(flattened_key, '')
                else:
                    p2 = "{}/{}".format(flattened_key, k)
                json_flattener(v2, p2)
        elif isinstance(v, list):
            for i, v2 in enumerate(v):
                p2 = "{}{}".format(flattened_key, i)
                json_flattener(v2, p2)
        else:
            return_list.append(["{}".format(flattened_key), v])

    json_flattener(obj)
    return return_list


def to_list(flat_list):
    dict = {}
    for i in range(len(flat_list)):
        if "count" in flat_list[i][0]:
            dict["0" + str(flat_list[i][0].split('/')[0])] = [flat_list[i][1], 0]
        elif "price" in flat_list[i][0]:
            dict["0" + str(flat_list[i][0].split('/')[0])][1] = flat_list[i][1]
    return dict


if __name__ == "__main__":
    sample1 = json.loads(
        requests.get("https://prod-storyly-media.s3.eu-west-1.amazonaws.com/test-scenarios/sample_1.json").content)
    sample2 = json.loads(
        requests.get("https://prod-storyly-media.s3.eu-west-1.amazonaws.com/test-scenarios/sample_2.json").content)
    sample3 = json.loads(
        requests.get("https://prod-storyly-media.s3.eu-west-1.amazonaws.com/test-scenarios/sample_3.json").content)
    print(to_list(json_cost_calculator(sample2)))
