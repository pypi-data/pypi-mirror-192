from setuptools import setup, find_packages

setup(
    name='QuykHtml',
    version='0.1.4',
    author='Marc D',
    author_email='marcwarrelldavis@yahoo.com',
    description='A python library that allows you to quickly and easily generate HTML templates and even create full-on websites.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mwd1993/QuykHtml',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)