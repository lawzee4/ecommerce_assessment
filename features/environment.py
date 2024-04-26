from django.test.runner import DiscoverRunner
from django.conf import settings

def before_all(context):
    settings.configure(DEBUG=True)  # Ensure the debug mode is on
    context.test_runner = DiscoverRunner()
    context.old_db_config = context.test_runner.setup_databases()

def after_all(context):
    context.test_runner.teardown_databases(context.old_db_config)
