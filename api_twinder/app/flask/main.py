from flask import Flask, render_template,request, redirect, url_for
from SVM_training import getResult
from collections import Counter
import twitter_api


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route("/showForm/", methods=["GET"])
def show_form():
    return render_template("template_user.html")

@app.route("/showTweets/", methods=["GET","POST"])
def show_list():
    tweets = list()
    predictions = list()
    if request.method == 'POST':
        user = request.form['usuarioTwitter']
        tweets = twitter_api.getuser(user)
        print("\n \n")
        print(40 * "+")
        print(tweets)
        predictions = getResult(tweets)
        print(predictions)

        #print(user)

        for tweet,prediction in zip(tweets,predictions):
            print(40 * "+")
            print(tweet)
            print("\n Prediction:", prediction)

        print(40 * "+")
        data = Counter(predictions)
        statistics = [(i, data[i] / len(predictions) * 100.0) for i in data.most_common()]

        print(statistics)
        print(40 * "+")


    return render_template("template_showTweets.html", user=user, tweets=tweets, predictions=predictions, size=len(tweets), statistics=statistics)

def getPercentage(predictions):

    for item in zip(predictions):
        c = Counter(item)
        total = sum(c.values())
        percent = {key: value / total for key, value in c.items()}
        print(percent)

        # convert to list
        percent_list = [percent.get(str(i), 0.0) for i in range(5)]
        print(percent_list)


def mostCommon(lst):
    data = Counter(lst)
    [(i, data[i] / len(lst) * 100.0) for i in data.most_common()]


# @app.route("/showSVM/", methods=["GET","POST"])
# def show_svm():
#     if request.method == 'POST':
#         user = request.form['usuarioTwitter']
#         tweets = twitter_api.getuser(user)
#         print(user)
#     return render_template("template_showSVM.html")

if __name__ == '__main__':
    app.run(debug=False)