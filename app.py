from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

def create_app():
    app = Flask(__name__)

    @app.route('/' ,methods=['GET', 'POST'])
    def connect_with_java():
        return "Flask Server & java are Working Successfully"
    
    # 이미지 수신 테스트용 blueprint
    from views import test_views
    app.register_blueprint(test_views.bp)

    return app

app = create_app()

if __name__ == "__main__":
    # app.config['TRAP_HTTP_EXCEPTIONS']=True
    # app.register_error_handler(Exception,serverErrorHandler)
    app.run(host='0.0.0.0', port = 5000 , debug=True)