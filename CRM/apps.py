from django.apps import AppConfig


class CrmConfig(AppConfig):
    name = 'CRM'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import CRM.signals_handlers