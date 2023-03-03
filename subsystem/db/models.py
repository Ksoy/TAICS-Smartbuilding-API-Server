from sqlalchemy.sql import func

from . import db


class TimestampMixin():
    # Ref: https://myapollo.com.tw/zh-tw/sqlalchemy-mixin-and-custom-base-classes/
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
        onupdate=func.now()
    )


class DictMixin():
    def to_dict(self, keys: list = None) -> dict:
        if keys is None:
            keys = map(lambda x: x.name, self.__table__.columns)
        return {k: getattr(self, k, None) for k in keys}


class Device(DictMixin, TimestampMixin, db.Model):
    ID = db.Column(db.String(20), primary_key=True)
    kind = db.Column(db.String(20), default='Device')
    tag = db.Column(db.Text)
    desc = db.Column(db.Text)
    type = db.Column(db.String(100))

    # loc
    locName = db.Column(db.String(100), nullable=True)
    locDesc = db.Column(db.Text, nullable=True)
    lat = db.Column(db.String(11), nullable=True)
    lon = db.Column(db.String(11), nullable=True)
    hgt = db.Column(db.String(11), nullable=True)
    elev = db.Column(db.String(100), nullable=True)
    roomTag = db.Column(db.String(100), nullable=True)
    floorName = db.Column(db.String(100), nullable=True)
    spaceName = db.Column(db.String(100), nullable=True)

    # meta
    vendor = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    SN = db.Column(db.String(100), nullable=True)
    fmwVer = db.Column(db.String(100), nullable=True)
    appVer = db.Column(db.String(100), nullable=True)
    URL = db.Column(db.String(100), nullable=True)
    spec = db.Column(db.Text, nullable=True)

    propertys = db.relationship(
        'Property',
        back_populates='device',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    @property
    def loc(self) -> dict:
        return self.to_dict(['locName', 'locDesc', 'lat', 'lon', 'hgt', 'refElev',
                             'elev', 'roomTag', 'floorName', 'spaceName'])

    @property
    def meta(self) -> dict:
        return self.to_dict(['vendor', 'model', 'SN', 'fmwVer', 'appVer', 'URL', 'spec'])

    @property
    def properties(self) -> dict:
        return {
            p.shortName: {'minimum': p.minimum, 'maximum': p.maximum}
            for p in self.propertys
        }


class Property(DictMixin, TimestampMixin, db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    shortName = db.Column(db.String(20))
    type = db.Column(db.String(20))
    minimum = db.Column(db.Float, nullable=True)
    maximum = db.Column(db.Float, nullable=True)

    DeviceID = db.Column(db.String(20), db.ForeignKey('device.ID'))
    device = db.relationship('Device', back_populates='propertys')

    values = db.relationship(
        'Value',
        back_populates='property',
        cascade='all, delete-orphan',
        lazy='dynamic',
        passive_deletes=True
    )


class Value(DictMixin, TimestampMixin, db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    PropertyID = db.Column(db.Integer, db.ForeignKey('property.id'))
    value = db.Column(db.Text)
    property = db.relationship('Property', back_populates='values')
