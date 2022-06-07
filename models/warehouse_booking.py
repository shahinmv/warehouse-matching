from db import db
from datetime import datetime

class WarehouseBooking(db.Model):
    __tablename__ = "warehouse_booking"

    id = db.Column(db.Integer, primary_key=True)

    merchant_id = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer)
    warehouse_owner_id = db.Column(db.Integer)
    r_storage = db.Column(db.Integer)
    check_in = db.Column(db.String(15))
    check_out = db.Column(db.String(15))
    goods_receiving_processing = db.Column(db.Boolean)
    labelling = db.Column(db.Boolean)
    manual_geo_data = db.Column(db.Boolean)
    item_picking = db.Column(db.Boolean)
    item_packaging = db.Column(db.Boolean)
    packaging_material = db.Column(db.Integer, default = 0)
    contracted = db.Column(db.Boolean)
    time_requested = db.Column(db.DateTime, default = datetime.now())

    def __init__(self, merchant, warehouse, owner, r_storage, check_in, check_out, goods_receiving_processing, item_picking, packaging_material):
        self.merchant_id = merchant
        self.warehouse_id = warehouse
        self.warehouse_owner_id = owner
        self.r_storage = r_storage
        self.check_in = check_in
        self.check_out = check_out
        self.goods_receiving_processing = goods_receiving_processing
        self.item_picking = item_picking
        self.packaging_material = packaging_material

    def set_labelling(self, labelling):
        self.labelling = labelling
    def set_manualgeo(self, manualgeo):
        self.manual_geo_data = manualgeo
    def set_itempackaging(self, itempackaging):
        self.item_packaging = itempackaging

    def contract(self, contract):
        self.contracted = contract
    
    def getTimeinMonth(self):
        x = self.time_requested
        test = x.strftime("%Y-%m-%d")
        print(x)
        return test
        

