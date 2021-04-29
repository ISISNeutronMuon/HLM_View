class HeliumDbRouter:
    """
    Custom router to control database operations on models in the HLM view app.
    """

    route_app_labels = {'hlmview'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read HLM_view models go to the helium database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'helium'
        return None
    
    def db_for_write(self, model, **hints):
        """
        Attempts to write HLM_view models go to the helium database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'helium'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Used by foreign key and many to many operations to determine if a relation should be allowed between two objects.
        If no router has an opinion (i.e. all routers return None), only relations within the same database are allowed.
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Determine if the migration operation is allowed to run on the database with alias db. 
        Return True if the operation should run, False if it shouldn’t run, or None if the router has no opinion.
        """
        if app_label in self.route_app_labels:
            return False
        return None
