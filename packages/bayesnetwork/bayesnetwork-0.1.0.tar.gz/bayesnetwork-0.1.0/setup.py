from setuptools import find_packages, setup
setup(
    name='bayesnetwork',
    version='0.1.0',
    author='Marco Jurado',
    author_email='marcojuradovelasquez2001@gmail.com',
    python_requires=">=3.6",
    description='Libreria de redes bayesianas para inferencia probabilistica.',
    long_description = open("README.md").read(),
    long_description_content_type ="text/markdown",
    packages= find_packages(where="src"),
    package_dir={"":"src","bayesnetwork":"src/bayesnetwork"},
    include_package_data=True,
    url="https://github.com/MaJu502/Inferencia-probabilistica",
    license='MIT',
    entry_points={"console_scripts":["bayesnetwork=bayesnetwork.bayesnetwork:main"]}
)