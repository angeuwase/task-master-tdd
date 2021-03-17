from project import create_app, db
#from project import db
#from project.models import User, Task

app = create_app()

#@app.shell_context_processor
#def make_shell_context():
#    return dict(db=db, User=User, Task=Task)

if __name__ == '__main__':
    app.run()