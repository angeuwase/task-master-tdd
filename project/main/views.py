from . import main_blueprint

@main_blueprint.route('/')
def index():
    return 'This will be a home page'