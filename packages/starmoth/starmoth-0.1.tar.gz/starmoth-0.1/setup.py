from setuptools import setup

setup(
    name="starmoth",
    version="0.1",
    author="Gudjon Magnusson",
    author_email="gmagnusson@fraunhofer.org",
    description="A small wrapper library to help test systems using STAR",
    long_description="STAR is system for systematically testing AI systems by intreating them with a combination of real and generated test data. To make an arbitrary system implementation testable with STAR we need a MOdel Test Harness, thats where MOTH comes in",
    url="",
    packages=["moth", "moth.cli", "moth.server", "moth.message", "moth.driver"],
    keywords="Fraunhofer, STAR, testing",
    python_requires=">=3.7, <4",
    install_requires=["pyzmq>=25.0.0", "numpy>=1.14.5", "msgpack>=1.0.4"],
    entry_points={
        "console_scripts": [
            "moth=moth.cli:cli",
        ]
    },
)
