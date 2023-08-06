import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RoboSmartServo", # Replace with your own username
    version="0.0.1",
    author="Example Author",
    author_email="kimjunseob1@roborobo.co.kr",
    description="Package for operating Smart Servos made by ROBOROBO in Seoul ROK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
