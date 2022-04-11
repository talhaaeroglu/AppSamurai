import requests
import json


def json_cost_calculator(obj, num):
    return_list = []

    def json_flattener(v, flattened_key=''):
        if isinstance(v, dict):
            for k, v2 in v.items():
                if k == "items" or k == "item":
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

    def to_list(flat_list):
        old_dict = {}
        sorted_dict = {}
        for i in range(len(flat_list)):
            if "count" in flat_list[i][0]:
                old_dict["0" + str(flat_list[i][0].split('/')[0])] = [flat_list[i][1], 0]
            elif "price" in flat_list[i][0]:
                old_dict["0" + str(flat_list[i][0].split('/')[0])][1] = flat_list[i][1]
        for k in sorted(old_dict, key=len, reverse=True):
            sorted_dict[k] = old_dict[k]
        return sorted_dict

    def cost_calculator(sorted_dict):
        for key, value in sorted_dict.copy().items():
            if value[1] != 0 and key != "0":
                parent_key = key[:-1]
                sorted_dict[parent_key][1] += value[0] * value[1]
                del sorted_dict[key]
        return "Sample{} top most cost is {}. Last calculation: Price:{} x Count:{} ".format(num, sorted_dict["0"][0] * sorted_dict["0"][1], sorted_dict["0"][1], sorted_dict["0"][0])

    json_flattener(obj)
    return cost_calculator(to_list(return_list))


if __name__ == "__main__":
    sample1 = json.loads(
        requests.get("https://prod-storyly-media.s3.eu-west-1.amazonaws.com/test-scenarios/sample_1.json").content)
    sample2 = json.loads(
        requests.get("https://prod-storyly-media.s3.eu-west-1.amazonaws.com/test-scenarios/sample_2.json").content)
    sample3 = json.loads(
        requests.get("https://prod-storyly-media.s3.eu-west-1.amazonaws.com/test-scenarios/sample_3.json").content)
    print(json_cost_calculator(sample1, 1))
    print(json_cost_calculator(sample2, 2))
    print(json_cost_calculator(sample3, 3))