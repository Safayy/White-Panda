from flask import Flask, render_template, request
from chatbot import chatbot

app=Flask(__name__)

@app.route("/", methods=['POST','GET'])
def calculate():
    output=''
    if request.method=='POST' and 'userInput' in request.form:
        input = request.form.get('userInput')
        #output = input+"ending now BOYYY"
        output = chatbot.chatuserLoop(input)
    return render_template('index.html',output=output)

'''
if __name__ == '__main__':
    app.run(debug=True) 
'''