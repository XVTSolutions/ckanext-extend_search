from sqlalchemy import *


class ReflectTest():

    def reflect_tables(self):

        engine = create_engine('postgresql://ckan_default:pass@localhost/ckan_default')

        metadata = MetaData()

        metadata.reflect(bind=engine)

        packages = metadata.tables['package']

        for p in packages:
            print p.name

        activities = metadata.tables['activity']

        for a in activities:
            print a.id
