import os
import openai
from flask import Flask, redirect, render_template, request, url_for
import json
from enum import Enum


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

class Api_Call(Enum):
    PRE_API_CALL, API_CALL_SUCCESS, API_CALL_FAILED = range(3)

@app.route("/", methods=("GET", "POST"))
def index():
    result = {'Claim': '', 'Supporting': '', 'Denying': '', 'IsThisTrue': '', 'Justification': '' }
    result_status = Api_Call.PRE_API_CALL
    input_text = 'Enter question here'
    if request.method == "POST":
        input_text = request.form["input_text"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": generate_prompt(input_text)}
            ]
        )
        try:
            result=json.loads(response.choices[0].message.content)
            result_status = Api_Call.API_CALL_SUCCESS
        except:
            result = response.choices[0].message.content
            result_status = Api_Call.API_CALL_FAILED
    
    return render_template("index.html", result=result, question=input_text, result_status=result_status)


def generate_prompt(input_text):
    return f"""
You are a fact-checking bot designed to validate \
if the claim <{input_text}> is verifiably true or false. \
To find out the veracity of the given claim do the following: \
- First, try to find 3 reputable sources supporting the claim. \
- Then, try to find 3 reputable sources denying the claim. \
- Based on the evidence provided in these sources \
and the reputability of these sources, determine \
if you believe the claim is verifiably true or false. \
- If you are not sure, specify whether you are more likely \
to believe the claim is false or true and by how much.

Make your conclusion on the veracity of the given claim \
based solely on the sources you found and your judgement \
of how reputable these sources are. \

Provide the following values in a valid JSON format according to the specified keys,
make sure to format the JSON properly:
{{ Key: "Claim", Value: <the given claim> \
Key: "Supporting", Value: <list of 3 sources supporting the claim cited in MLA format> \
Key: "Denying", Value: <list of 3 sources denying the claim cited in MLA format> \
Key: "IsThisTrue", Value: <Yes, No, or Maybe> \
Key: "Justification", Value: <your elaboration on why the claim is true, false, or uncertain \
and how the sources support your argument. \
use less than 200 words and target your response for an average person.> }}"""
