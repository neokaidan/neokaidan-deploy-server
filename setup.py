from setuptools import find_packages
from setuptools import setup

setup(
    name="deployment_server",
    version="0.1.0",
    description="Daemon server on VPS for CD part in GutHub Actions",
    author="Neokaidan",
    packages=["server"],
    install_requires=["Flask", "docker", "python-dotenv"],
    entry_points={"console_scripts": ["gacd_daemon = server.main:main"]},
)
