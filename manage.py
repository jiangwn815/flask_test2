# from flask.ext.script import Manager, Server
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app import db
from app.models import Role, User


# from app.models import Post
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
#manager.add_command("Server", Server(host="127.0.0.1", port=5000, use_debugger=True))

if __name__ == '__main__':
    manager.run()
