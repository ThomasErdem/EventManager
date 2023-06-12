from event_app import db

def do_create(do_drop=False):
    # from file import object
    from event_app.bp_events.model_event import Event
    #from bp_users import User
    
    if do_drop is True:
        db.drop_all()
    
    db.create_all()