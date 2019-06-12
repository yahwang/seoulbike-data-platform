class BikeStationRouter:

    def db_for_read(self, model, **hints):
        """Send all read operations on bike_stations app models to `bike_db`."""
        if model._meta.app_label == 'bike_stations':
            return 'bike_db'
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on bike_stations app models to `bike_db`."""
        if model._meta.app_label == 'bike_stations':
            return 'bike_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the Example app's models get created on the right database."""
        if app_label == 'bike_stations':
            # The bike_stations app should be migrated only on the bike_db database.
            return db == 'bike_db'
        elif db == 'bike_db':
            # Ensure that all other apps don't get migrated on the bike_db database.
            return False

        # No opinion for all other scenarios
        return None

'''
    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""

        # Allow any relation between two models that are both in the Example app.
        if obj1._meta.app_label == 'example' and obj2._meta.app_label == 'example':
            return True
        # No opinion if neither object is in the Example app (defer to default or other routers).
        elif 'example' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Block relationship if one object is in the Example app and the other isn't.
            return False
'''