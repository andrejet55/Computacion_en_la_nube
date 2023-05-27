import urllib.request
import json
import os
import ssl

from flask import Flask,request,render_template,abort,jsonify

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script





application=Flask(__name__)

app=application

## Route for a home page


def recorte(cadena):
    entrada=cadena.decode('UTF-8')
    salida=entrada[61:]
    salida2=salida[:salida.rfind('"')]
    return salida2


class CustomData:
    def __init__(  self,
        Gender: str,
        Age: float,
        Height:float,
        Weight:float,
        family_history_with_overweight:str,
        FAVC:str,
        FCVC:int,
        NCP:int,
        CAEC:str,
        SMOKE:int,
        CH2O:int,
        SCC:str,
        FAF:int,
        TUE:int,
        CALC:str,
        MTRANS:str):
        
        self.Gender=Gender
        self.Age=Age
        self.Height=Height
        self.Weight=Weight
        self.family_history_with_overweight=family_history_with_overweight
        self.FAVC=FAVC
        self.FCVC=FCVC
        self.NCP=NCP
        self.CAEC=CAEC
        self.SMOKE=SMOKE
        self.CH2O=CH2O
        self.SCC=SCC
        self.FAF=FAF
        self.TUE=TUE
        self.CALC=CALC
        self.MTRANS=MTRANS
       


    def get_data(self):
        
        custom_data_input_dict = {
            "Gender": self.Gender,
            "Age" :   self.Age,
            "Height":self.Height,
            "Weight":self.Weight,
            "family_history_with_overweight":self.family_history_with_overweight,
            "FAVC":self.FAVC,
            "FCVC":self.FCVC,
            "NCP":self.NCP,
            "CAEC":self.CAEC,
            "SMOKE":self.SMOKE,
            "CH2O":self.CH2O,
            "SCC":self.SCC,
            "FAF":self.FAF,
            "TUE":self.TUE,
            "CALC":self.CALC,
            "MTRANS":self.MTRANS,
            }

        return custom_data_input_dict

       



@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='GET':
        return render_template('index.html')
    else:
        data=CustomData(
            Gender=request.form.get('Gender'),
            Age=request.form.get('Age'),
            Height=float(request.form.get('Height')),
            Weight=float(request.form.get('Weight')),
            family_history_with_overweight=request.form.get('family_history_with_overweight'),
            FAVC=request.form.get('FAVC'),
            FCVC=request.form.get('FCVC'),
            NCP=request.form.get('NCP'),
            CAEC=request.form.get('CAEC'),
            SMOKE=request.form.get('SMOKE'),
            CH2O=request.form.get('CH2O'),
            SCC=request.form.get('SCC'),
            FAF=request.form.get('FAF'),
            TUE=request.form.get('TUE'),
            CALC=request.form.get('CALC'),
            MTRANS=request.form.get('MTRANS'))
                          
            
        pred=data.get_data()
        print(pred)
        
        
        info =  {
          "Inputs": {
            "WebServiceInput0": [pred]
          },
          "GlobalParameters": {}
        }
        
        
        body = str.encode(json.dumps(info))

        url = 'http://3dd4867d-54ee-49ee-aeec-6cd5bbe8f39c.australiaeast.azurecontainer.io/score'
        # Replace this with the primary/secondary key or AMLToken for the endpoint
        api_key = 'nyj84tb7VSA3CiqlTeL92I6P2ijf4y5A'
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")


        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            print(result)
            salida=recorte(result)
            
            
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))
        
        return render_template('index.html',results=salida)
       
       
if __name__=="__main__":      
    #app.run(host="0.0.0.0",port=80)
    app.run()