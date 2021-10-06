from setuptools import find_packages, setup

setup(
    name='seft_203_api',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-jwt-extended',
        'flask-restful',
        'flask-sqlalchemy',
        'flask-bcrypt',
    ],
)