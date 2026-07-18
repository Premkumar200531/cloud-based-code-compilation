
from flask import Flask
from config import Config
from database import db
from models import User, Language
from flask_login import LoginManager
from flask_cors import CORS
from flask_migrate import Migrate

def create_app():
    app = Flask()
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from routes.code import code_bp as code_blueprint
    app.register_blueprint(code_blueprint, url_prefix='/api')

    from routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        
        # Seed default admin if not exists
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@compiler.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

        # Seed languages if empty
        if not Language.query.first():
            import sys
            # Python
            py = Language(name='Python', version='3.x', run_cmd=f'"{sys.executable}" "{{file}}"', is_active=True)
            # JavaScript (Node)
            js = Language(name='JavaScript', version='Node', run_cmd='node "{file}"', is_active=True)
            # C (GCC)
            c = Language(name='C', version='GCC', compile_cmd='gcc "{file}" -o "{out}"', run_cmd='"{out}"', is_active=True)
            # C++ (G++)
            cpp = Language(name='C++', version='G++', compile_cmd='g++ "{file}" -o "{out}"', run_cmd='"{out}"', is_active=True)
            # Java
            java = Language(name='Java', version='11+', compile_cmd='javac "{file}"', run_cmd='java -cp "{dir}" "{class}"', is_active=True)
            
            db.session.add(py)
            db.session.add(js)
            db.session.add(c)
            db.session.add(cpp)
            # db.session.add(java) # Skipping Java for MVP simplicity unless JDK is confirmed
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
=======
from flask import Flask
from config import Config
from database import db
from models import User, Language
from flask_login import LoginManager
from flask_cors import CORS
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from routes.code import code_bp as code_blueprint
    app.register_blueprint(code_blueprint, url_prefix='/api')

    from routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        
        # Seed default admin if not exists
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@compiler.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

        # Seed languages if empty
        if not Language.query.first():
            import sys
            # Python
            py = Language(name='Python', version='3.x', run_cmd=f'"{sys.executable}" "{{file}}"', is_active=True)
            # JavaScript (Node)
            js = Language(name='JavaScript', version='Node', run_cmd='node "{file}"', is_active=True)
            # C (GCC)
            c = Language(name='C', version='GCC', compile_cmd='gcc "{file}" -o "{out}"', run_cmd='"{out}"', is_active=True)
            # C++ (G++)
            cpp = Language(name='C++', version='G++', compile_cmd='g++ "{file}" -o "{out}"', run_cmd='"{out}"', is_active=True)
            # Java
            java = Language(name='Java', version='11+', compile_cmd='javac "{file}"', run_cmd='java -cp "{dir}" "{class}"', is_active=True)
            
            db.session.add(py)
            db.session.add(js)
            db.session.add(c)
            db.session.add(cpp)
            # db.session.add(java) # Skipping Java for MVP simplicity unless JDK is confirmed
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
