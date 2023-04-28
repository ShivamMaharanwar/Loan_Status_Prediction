from flask import Flask , jsonify , request
import pickle
import pandas as pd 
import numpy as np
import mysql.connector as sql

app = Flask(__name__)

mydb = sql.connect(host='localhost',
                  user = 'root',
                  passwd ='14920151',
                  use_pure = True
                  )
                  
print(mydb)
mycursor = mydb.cursor()


rf_model = pickle.load(open('rf_model.pkl','rb'))

@app.route('/')
def main():
    return jsonify({'Message':'Model is Activated'})


       
@app.route('/Loan_Approval_system',methods = ['POST','GET'])
def loan_approval_prediction():
    global data
    data = request.get_json()
    Gender = data['Gender']
    print(Gender)
    Married = data['Married']
    print(Married)
    Dependents = data['Dependents']
    print(Dependents)
    Education = data['Education']
    print(Education)
    Self_Employed = data['Self_Employed']
    print(Self_Employed)
    ApplicantIncome = data['ApplicantIncome']
    print(ApplicantIncome)
    CoapplicantIncome = data['CoapplicantIncome']
    print(CoapplicantIncome)
    LoanAmount = data['LoanAmount']
    print(LoanAmount)
    Loan_Amount_Term = data['Loan_Amount_Term']
    print(Loan_Amount_Term)
    Credit_History = data['Credit_History']
    print(Credit_History)
    Property_Area = data['Property_Area']
    print(Property_Area)
    
    
    
    """'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
       'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
       'Loan_Amount_Term', 'Credit_History', 'Property_Area'"""
    
    d = {'Gender':[Gender],
         'Married':[Married],
         'Dependents':[Dependents],
         'Education':[Education],
         'Self_Employed':[Self_Employed],
         'ApplicantIncome':[ApplicantIncome],
         'CoapplicantIncome':[CoapplicantIncome],
         'LoanAmount':[LoanAmount],
         'Loan_Amount_Term':[Loan_Amount_Term],
         'Credit_History':[Credit_History],
         'Property_Area':[Property_Area]}
         
    
    
    input = pd.DataFrame(d)
    
    prediction = rf_model.predict(input)
    
    insert_query = ("""INSERT INTO loan_data.new_loan_data(Gender,
    Married,
    Dependents,
    Education,
    Self_Employed,
    ApplicantIncome,
    CoapplicantIncome,
    LoanAmount,
    Loan_Amount_Term,
    Credit_History,
    Property_Area
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """)
    data1 = (data['Gender'],data['Married'],data['Dependents'],data['Education'],data['Self_Employed'],data['ApplicantIncome'],
             data['CoapplicantIncome'],data['LoanAmount'],data['Loan_Amount_Term'],data['Credit_History'],data['Property_Area'])

    try:
        mycursor.execute(insert_query,data1)
        mydb.commit()
        print('we are in try block')
    except:
        mydb.rollback()
        print('We are in except block')
        
        
    return jsonify({'Approval Status': prediction[0]})

if __name__ == '__main__':
    app.run(debug = True)
    
    
    
    
    