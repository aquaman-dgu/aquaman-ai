from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate

app = Flask(__name__)

def create_app():
    @app.route('/' ,methods=['GET', 'POST'])
    def connect_with_java():
        return "Flask Server & java are Working Successfully"
    return app

app = create_app()

if __name__ == "__main__":
    # app.config['TRAP_HTTP_EXCEPTIONS']=True
    # app.register_error_handler(Exception,serverErrorHandler)
    app.run(host='0.0.0.0', port = 5000 , debug=True)