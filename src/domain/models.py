import datetime

from peewee import *
from src.adapters.db_conection import db


class BaseModel(Model):
    created_at = DateTimeField()
    updated_at = DateTimeField(null=True)

    class Meta:
        database = db

    def save_model(self):
        if db.is_closed():
            db.connect()
        self.created_at = datetime.datetime.now()
        self.save()

    def update_model(self):
        if db.is_closed():
            db.connect()
        self.updated_at = datetime.datetime.now()
        self.save()


class DocumentType(BaseModel):
    name = CharField(primary_key=True)


class Farmer(BaseModel):
    document = CharField(max_length=14, primary_key=True)
    document_type = ForeignKeyField(DocumentType, to_field='name')
    name = CharField(max_length=255)

    def create_new(self, name, document, document_type):
        if db.is_closed():
            db.connect()
        return self.create(name=name,
                           document=document,
                           document_type=document_type,
                           created_at=datetime.datetime.now())

    def delete_farmer(self):
        if db.is_closed():
            db.connect()
        self.delete()

    def get_input_values(self):
        return {'name': self.name if self.name else '',
                'document': self.document if self.document else '',
                'document_type': self.document_type if self.document_type else ''}

    def update_model(self):
        if db.is_closed():
            db.connect()
        self.updated_at = datetime.datetime.now()
        self.save()

    @staticmethod
    def has_farmer(document):
        return True if Farmer.select().where(Farmer.document == document) else False

    @staticmethod
    def get_farmer(document):
        has_farmer = Farmer.select().where(Farmer.document == document)
        if has_farmer:
            return has_farmer.get()
        return None


class Farm(BaseModel):
    farm_id = AutoField(primary_key=True)
    name = CharField(max_length=120, unique=True)
    farmer_owner = ForeignKeyField(Farmer, to_field='document', on_delete='cascade')
    city = CharField(max_length=120)
    state = CharField(max_length=2)
    total_area = FloatField()
    agricultural_area = FloatField()
    vegetation_area = FloatField()

    def create_new(self, **kwargs):
        if db.is_closed():
            db.connect()
        return self.create(**kwargs)

    @staticmethod
    def get_farms_tuple(farmer_id):
        farms_name = []
        for farm in Farm.select().where(Farm.farmer_owner == farmer_id):
            farms_name.append(farm.name)
        return tuple(farms_name)

    @staticmethod
    def has_farm(farm_name):
        return True if Farm.select().where(Farm.name == farm_name) else False

    @staticmethod
    def get_farm_count(farmer_id=None):
        if farmer_id:
            return Farm.select().where(Farm.farmer_owner==farmer_id).count()
        return Farm.select().count()

    @staticmethod
    def get_farm_total_area(farmer_id=None):
        if farmer_id:
            return Farm.select(fn.SUM(Farm.total_area)).where(Farm.farmer_owner == farmer_id).scalar()
        return Farm.select(fn.SUM(Farm.total_area)).scalar()

    @staticmethod
    def get_farm_group_by_state():
        result = {}
        for query in Farm.select(Farm.state, fn.Count(Farm.state).alias('amount')).group_by(Farm.state):
            result[query.state] = query.amount
        return result

    @staticmethod
    def get_farm_group_by_soil_use(farm_id=None):
        result = {}
        for query in Farm.select(fn.Sum(Farm.vegetation_area).alias('vegetation_area'), fn.Sum(Farm.agricultural_area).alias('agricultural_area')):
            result['Area de Vegetação'] = query.vegetation_area
            result['Area Agricultável'] = query.agricultural_area
        return result


class CultureType(BaseModel):
    culture_type_name = CharField(primary_key=True)

    @staticmethod
    def get_cultures_tuple():
        culture_labels = []
        for culture_type in CultureType.select():
            culture_labels.append(culture_type)
        return tuple(culture_labels)


class Culture(BaseModel):
    farm = ForeignKeyField(Farm, to_field='farm_id', on_delete='cascade')
    culture_type = ForeignKeyField(CultureType, to_field='culture_type_name')

    @staticmethod
    def get_farm_culture(farm_id):
        return [culture.culture_type for culture in Culture.select().where(Culture.farm == farm_id)]

    @staticmethod
    def get_farm_group_by_culture():
        result = {}
        for query in Culture.select(Culture.culture_type, fn.Count(Culture.culture_type).alias('amount')).group_by(Culture.culture_type):
            result[query.culture_type] = query.amount
        return result

if __name__ == '__main__':
    # db.create_tables([DocumentType, Farmer, Farm, CultureType, Culture])
    Farm.get_farm_group_by_soil_use()