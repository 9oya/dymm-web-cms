from setuptools import setup

setup(
    name='dymm_cms',
    packages=['dymm_cms'],
    include_package_data=True,
    install_requires=[
        'flask',
        'blinker',
        'requests',
        'Flask-WTF',
        'Flask-SQLAlchemy',
        'psycopg2-binary',
        'pytz',
        'Flask-Excel',
        'declxml',
        'pyexcel',
        'pyexcel-xls',
        'pyexcel-xlsx',
        'pyexcel-handsontable',
        'jsonschema',
        'Flask-Bcrypt',
        'Flask-JWT-Extended',
        'Flask-Mail',
        'sqlacodegen'
        'google-cloud-storage'
    ]
)
