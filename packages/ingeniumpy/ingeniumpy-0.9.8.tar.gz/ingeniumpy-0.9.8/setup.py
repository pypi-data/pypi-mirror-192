import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# find . -name '*.pyc' -delete
# python3 setup.py sdist
# python3 -m pip install --user --upgrade twine
# cd dist
# python3 -m twine upload <file>

# Version notes:
# 0.5.0-0.6.0 -> GijonIN OLD
# 0.6.1 -> GijonIN
# 0.7.0 -> CalidadAire
# 0.7.{1,2} -> CalidadAire cambios
# 0.8.0 -> 6LowPan
# 0.8.6 -> Valores 87, 88, 89 de Sock
# 0.8.9 -> Updated proxy dependencies
# 0.8.10 -> Updated naming when id is repeated
# 0.8.14 -> No poll when no devices
# 0.8.15 -> Catch timeout exception
# 0.8.16 -> Catch timeout exception during login
# 0.8.18 -> Sif bat baja
# 0.8.19 -> Añadido state
# 0.8.20 -> Arreglada intensidad y potencia reactiva cuando consumo es 0
# 0.8.21 -> Meterbus factor
# 0.8.22 -> Socks detect file
# 0.8.24 -> Added noise sensor
# 0.8.25 -> Token hass websocket como env
# 0.8.32 -> Filtering socket voltage readings
# 0.8.37 -> Soporte temperatura CO2
# 0.9.0  -> Removed Hass integration
# 0.9.4  -> 3fase meter
# 0.9.8  -> Alarmas

setuptools.setup(
    name="ingeniumpy",
    version="0.9.8",
    author="Daniel Garcia",
    author_email="dgarcia@ingeniumsl.com",
    description="Ingenium API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/ingeniumpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Home Automation",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.6,<4.0",
    ],
    package_data={"ingeniumpy": ["bin/proxy*"]},
)
