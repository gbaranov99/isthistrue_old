import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    result = ''
    input_text = 'Enter question here'
    if request.method == "POST":
        input_text = request.form["input_text"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": input_text}
            ]
        )
        result=response.choices[0].message.content
    
    return render_template("index.html", result=result, question=input_text)


def generate_prompt(input_text):
    return """I've heard that {}. Is this true? 
What evidence supporting or disproving this claim can you provide?"""
