import pkg_resources
import requests
import json
from distutils.version import StrictVersion

this_version = pkg_resources.get_distribution('mattuni').version

# https://stackoverflow.com/a/27239645/6596010
def versions(package_name):
    url = "https://pypi.org/pypi/%s/json" % (package_name,)
    data = json.loads(requests.get(url).text)
    versions = list(data["releases"].keys())
    versions.sort(key=StrictVersion)
    return versions

online_versions = versions("mattuni")
latest_version = online_versions[len(online_versions)-1]
if (this_version != latest_version):
    print(f"WARNING: You are using mattuni {this_version} but the latest version is {latest_version}. In the terminal use `python -m pip install mattuni --upgrade` to update.")

_ran_x_times = []
def send_answer(question_number,answer):
    print()
    print()
    global _ran_x_times
    if question_number in _ran_x_times:
        print(f"Challenge {question_number} Failed. You can only call send_answer one time per challenge.")
    else:
        _ran_x_times.append(question_number)
        if (len(answer) < 200):
            print(f"Sending answer for question {question_number} to the server: \"" + answer + "\" ...")
        else:
            print(f"Sending the (very long) answer for question {question_number} to the server...")
        j = json.dumps({
            "q": question_number,
            "answer": answer
        })
        response = requests.get('https://teach-anya.herokuapp.com/send', data=str.encode(j))
        print(response.text)
        print()
        print()



def get_input(question_number):
    print(f"Getting json input for question {question_number} ...")
    j = json.dumps({
        "q": question_number,
    })
    response = requests.get('https://teach-anya.herokuapp.com/get-big-input', data=str.encode(j))
    r = response.text
    print(f"Got json input (length={len(response.text)}) Don't forget to decode it!")
    return r