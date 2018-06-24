from django.apps import AppConfig


class CalendarConfig(AppConfig):
    name = 'Calendar'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import Calendar.signals_signals