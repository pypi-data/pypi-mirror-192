import re
from setuptools import setup

#with open('requirements.txt') as f:
#    requirements = f.read().splitlines()

#with open('4chan/__init__.py') as f:
#    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)[1] # type: ignore

#with open('README.md', encoding='utf-8') as f:
#    readme = f.read()

#extras_require = {
#    'docs': [
#        'Sphinx==4.4.0',
#        'furo==2022.2.23'
#    ],
#    'test': [
#        'pytest==7.1.1'
#    ],
#}

setup(
    name='4chan.py',
    author='scrazzz',
    url='https://github.com/scrazzz/4chan.py',
    project_urls={
        'Documentation': 'https://github.com/scrazzz/4chan',
        'Issue tracker': 'https://github.com/scrazzz/4chan.py/issues'
    },
    version='0.0.0',
    packages=['4chan'],
    ########extras_require=extras_require,
    license='MIT',
    description='',
    #long_description=readme,
    #long_description_content_type='text/markdown',
    include_package_data=True,
    #install_requires=requirements,
    python_requires='>=3.8.0',
)
