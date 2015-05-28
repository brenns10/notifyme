from setuptools import setup

long_description = open('README.rst').read()

setup(
    name='notifyme',
    version='0.1',
    description='Email notifications on task completion',
    long_description=long_description,
    url='https://github.com/brenns10/notifyme',
    author='Stephen Brennan',
    author_email='stephen@stephen-brennan.com',
    license='Revised BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Email :: Email Clients (MUA)',
        'Topic :: Utilities',
    ],
    keywords='notify notifications email',
    entry_points={
        'console_scripts': [
            'notifyme=notifyme:_main',
        ],
    },
)
