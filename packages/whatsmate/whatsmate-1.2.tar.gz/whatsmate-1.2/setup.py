from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='whatsmate',
    version='1.2',
    description='The ultimate WhatsApp Wrapper for Python',
    author='Harsh Vardhan Goswami',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='me@iamharsh.dev',
    packages=['whatsmate'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='whatsapp automation chatbot api',
    license='MIT',
    url='https://github.com/iamharshdev/whatsmate',
)
