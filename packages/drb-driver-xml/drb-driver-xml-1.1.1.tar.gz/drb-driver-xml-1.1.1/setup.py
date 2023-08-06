import versioneer
from setuptools import find_namespace_packages, setup


with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='drb-driver-xml',
    packages=find_namespace_packages(include=['drb.*']),
    description='DRB XML implementation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://gitlab.com/drb-python/impl/xml',
    install_requires=REQUIREMENTS,
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",

    ],
    python_requires='>=3.8',
    entry_points={
        'drb.driver': 'xml = drb.drivers.xml:XmlNodeFactory',
        'drb.topic': 'xml = drb.topics.xml',
    },
    version=versioneer.get_version(),
    package_data={
        'drb.topics.xml': ['cortex.yml']
    },
    data_files=[('.', ['requirements.txt'])],
    cmdclass=versioneer.get_cmdclass(),
    project_urls={
        'Documentation': 'https://drb-python.gitlab.io/impl/xml',
        'Source': 'https://gitlab.com/drb-python/impl/xml',
    }
)
