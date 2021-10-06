from seft_203_api.api import create_app


app = create_app() 
app.run(debug=True, host='0.0.0.0')