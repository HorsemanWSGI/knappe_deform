from setuptools import setup


setup(
    name='knappe_deform',
    install_requires = [
        'knappe',
        'chameleon',
        'deform',
        'colander'
    ],
    extras_require={
        'test': [
            'WebTest',
            'pytest',
            'pyhamcrest',
        ]
    }
)
