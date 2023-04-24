from setuptools import find_packages
from setuptools import setup
import server

setup(
    name="gacd_server",
    version=server.__version__,
    description="Daemon server on VPS for CD part in GutHub Actions",
    author="Neokaidan",
    packages=["server"],
    install_requires=["Flask", "docker", "python-dotenv"],
    entry_points={"console_scripts": ["gacd_server = server.main:main"]},
)
