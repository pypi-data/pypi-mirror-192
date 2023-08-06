import requests
import json
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