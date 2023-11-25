import logging

from model.config.core import PACKAGE_ROOT, config

# Aquí definimos un logger para el paquete, y usamos solamente el 
# NullHandler para no restringir los logger para las aplicaciones que 
# usen el modelo empaquetado. 
# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger(config.app_config.package_name).addHandler(logging.NullHandler())


with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()
