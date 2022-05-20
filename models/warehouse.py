from db import db

class Warehouse(db.Model):
    __tablename__ = 'PilotApp_warehouse_test'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50))
    volume_available = db.Column(db.Integer)
    volume_total = db.Column(db.Integer)
    labelling = db.Column(db.Boolean)
    manual_geo_data_entry = db.Column(db.Boolean)
    item_packaging = db.Column(db.Boolean)
    palette_packaging = db.Column(db.Boolean)
    address = db.Column(db.String(200))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))

    warehouse_services = db.relationship('WarehouseServices', lazy='dynamic')

    def __init__(self, name, volume_available, volume_total, labelling, manual_geo_data_entry, item_packaging, palette_packaging, address, email, phone):
        self.name = name
        self.volume_available = volume_available
        self.volume_total = volume_total
        self.labelling = labelling
        self.manual_geo_data_entry = manual_geo_data_entry
        self.item_packaging = item_packaging
        self.palette_packaging = palette_packaging
        self.address = address
        self.email = email
        self.phone = phone
