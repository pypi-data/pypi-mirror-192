from setuptools import setup

setup(
    name="what_a_weather",
    packages=["what_a_weather"],
    version="0.1.0",
    license="MIT",
    description="Next 12 hour weather forecast data",
    author="Cihat Ertem",
    author_email="cihatertem+weather_app@gmail.com",
    url="https://cihatertem.dev",
    keywords=["what_a_weather", "weather", "forecast", "opeweathermap",
              "openweather"],
    requires=["requests"],
    requires_python=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)
