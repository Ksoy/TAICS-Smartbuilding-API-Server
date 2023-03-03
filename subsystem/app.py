import json

from flask import Flask
from flask import jsonify

from . import config
from .db import db
from .db import models
from .devices_app import devices_app
from .event_app import event_app


def start_server():
    config.read_config()
    app = Flask(__name__)

    @app.route("/")
    def index():
        res = jsonify({'text': "Hello World!"})
        return res

    app.register_blueprint(devices_app, url_prefix='/devices')
    app.register_blueprint(event_app, url_prefix='/event')

    # Configure Flask-SQLAlchemy
    # Ref: https://tinyurl.com/26dbers4
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.BASE_DIR}/sqlite.db'
    # Ref: https://tinyurl.com/9umn83fe
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

        if models.Device.query.count() == 0:
            init_db()

    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


def init_db():
    with open(f'{config.BASE_DIR}/devices.json') as f:
        devices = json.loads(f.read())

    for d in devices:
        new_device = models.Device(
            ID=d.get('ID'),
            kind=d.get('kind'),
            tag=d.get('tag'),
            desc=d.get('desc'),
            type=d.get('type'),
            **d.get('loc', {}),
            **d.get('meta', {}),
        )
        db.session.add(new_device)
        db.session.commit()

        for short_name, p in d.get('Properties', {}).items():
            new_property = models.Property(
                shortName=short_name,
                type=p.get('type', 'string'),
                minimum=p.get('minimum'),
                maximum=p.get('maximum'),
                device_id=d.get('ID'),
            )
            db.session.add(new_property)
            db.session.commit()

            if 'value' in p:
                new_value = models.Value(
                    PropertyID=new_property.id,
                    value=p.get('value')
                )
                db.session.add(new_value)
                db.session.commit()

    db.session.commit()
