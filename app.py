from functionDefined import cap_cal
from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('./homePage.html')



@app.route('/', methods=['POST'])
def my_form_post():
    J = request.form['J']
    H = request.form['H']
    M = request.form['M']
    L = request.form['L']
    A = request.form['A']
    B = request.form['B']
    C = request.form['C']
    D = request.form['D']
    E = request.form['E']
    ROT1 = request.form['ROT1']
    ROT2 = request.form['ROT2']
    ROT3 = request.form['ROT3']
    ROT4 = request.form['ROT4']
    ROT5 = request.form['ROT5']
    S = request.form['S']
    l = request.form['l']
    w = request.form['w']
    r = cap_cal(J,H,M,L,A,B,C,D,E,ROT1,ROT2,ROT3,ROT4,ROT5,S,l,w)
    f = "The capacity envelop points are: " + str(r["numberOfDeparturesToBeInserted"]) + "---" + str(r["departuresOnlyCapacity"]) + "---" + str(r["arrivalsOnlyCapaciy"])
    return render_template('./returnPage.html', obj=r)
if __name__ == "__main__":
    app.run()