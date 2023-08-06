import logging


def setup_environment(code_bucket):
    import os
    import sys
    import inspect
    from pathlib import Path

    from rich.console import Console
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO, format="%(message)s", datefmt="[%X]",
        handlers=[RichHandler(console=Console(stderr=True))]
    )
    log = logging.getLogger("rich")
    log.setLevel(logging.INFO)

    current_directory = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))

    settings_file = Path(current_directory) / 'downloaded_settings.py'

    logging.info('Settings file downloading to: '
                 '{}'.format(settings_file))

    import boto3
    s3client = boto3.client('s3')
    s3client.download_file(code_bucket, 'settings.py', str(settings_file))

    sys.path.append(current_directory)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'downloaded_settings')

    import django
    django.setup()
