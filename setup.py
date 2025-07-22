from setuptools import setup

setup(
   name='apply',
    version='1.0.0',
    py_modules=['apply'],
    install_requires=['paramiko'],
    entry_points={
       'console_scripts': [
          'apply=apply:main',  # Format: command=module:function
       ],
    },
    author = 'Ed Ruszkiewicz',
    author_email = 'ed@ruszkiewicz.net',
    description = 'Batch Command Grab vis SSH',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ruszkiew/apply',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
