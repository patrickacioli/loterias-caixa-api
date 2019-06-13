import pyrebase

config = {
  "apiKey": "apiKey",
  "authDomain": "caixabot-9893f.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "caixabot-9893f.appspot.com",
  "serviceAccount": "path/to/serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)