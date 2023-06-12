import click
from flask.cli import with_appcontext
from event_app.bp_home import bp_general 

@bp_general.cli.command('create-db')
@with_appcontext
def do_create_db():
    from event_app.bp_home.helpers import do_create
    do_create()




