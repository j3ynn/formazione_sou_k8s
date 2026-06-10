from flask import Flask # libreria Flask 

app = Flask(__name__) # salviamo l'applicazione nella variabile app

@app.route("/") # collega l'url alla funzione (sotto). decorator @ = quando qualcuno visita la pagina. 
def hello(): # funzione hello
    return "Hello World!" # ritorna questa stringa

if __name__ == '__main__': # se questo file è stato eseguito avvia l'applicazione 
    app.run(host='0.0.0.0', port=8000) # avvia il server

