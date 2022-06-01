from cgitb import strong
from db import db

class WarehouseServices(db.Model):
    __tablename__ = 'PilotApp_warehouseservice_test'

    id = db.Column(db.Integer, primary_key=True)

    storage = db.Column(db.Integer)
    goods_receiving_processing = db.Column(db.Integer)
    goods_receiving_labelling = db.Column(db.Integer)
    goods_receiving_manuel_geo_data = db.Column(db.Integer)
    item_picking = db.Column(db.Integer)
    item_packaging = db.Column(db.Integer)
    palette_packaging = db.Column(db.Integer)
    packaging_material = db.Column(db.Integer)
    
    warehouse_id = db.Column(db.Integer, db.ForeignKey('PilotApp_warehouse_test.id'))

    def __init__(self, storage, item_picking, goods_receiving_processing, packaging_material, warehouse_id):
        self.storage = storage
        self.item_picking = item_picking
        self.goods_receiving_processing = goods_receiving_processing
        self.packaging_material = packaging_material
        self.warehouse_id = warehouse_id

    def set_labelling(self, goods_receiving_labelling):
        self.goods_receiving_labelling = goods_receiving_labelling
    
    def set_manualgeodata(self, goods_receiving_manuel_geo_data):
        self.goods_receiving_manuel_geo_data = goods_receiving_manuel_geo_data
    
    def set_item(self, item_packaging):
        self.item_packaging = item_packaging

    def set_packaging(self, palette_packaging):
        self.palette_packaging = palette_packaging