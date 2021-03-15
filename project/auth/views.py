from . import auth_blueprint

@auth_blueprint.route('/register')
def register():
    return 'This will be a registration page'