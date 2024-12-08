from flask import Flask, render_template
from flask_cors import CORS
from app.services.llm_service import LLMService
import logging
import sys



def create_app():
    app = Flask(__name__)

    # initialize CORS
    CORS(app)

    # set up logging
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)
    
    with app.app_context():
        llm_service = LLMService()
        app.llm_service = llm_service
    
    # register blueprints
    from app.api import chat_bp, analysis_bp
    app.register_blueprint(chat_bp)
    app.register_blueprint(analysis_bp)
    
    # 主页路由可以保留在主应用中
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app