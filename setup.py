from setuptools import setup, find_packages

setup(
    name='gptbatcher',
    version='0.1.1',
    url='https://github.com/CBM-Digital/GPTBatcher',
    author="James O'Toole",
    author_email='jamesotoole@cbmdigital.co.uk',
    description='Conduct surveys using GPT',
    long_description=open('README.md').read(),
    packages=find_packages(),    
    install_requires=[
        'openai>=1.12.0',
        'pandas',
    ],
)
