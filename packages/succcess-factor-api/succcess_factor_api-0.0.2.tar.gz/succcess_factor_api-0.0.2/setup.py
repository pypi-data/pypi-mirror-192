import json
from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

package_json_path = f"{this_directory}/package.json"
package_json_content = Path(package_json_path).read_text()
current_version = json.loads(package_json_content)['version']

setup(
    name='succcess_factor_api',
    version=current_version,
    packages=find_packages(),
    author='Jonathan Rodriguez Alejos',
    author_email='jrodriguez.5716@gmail.com',
    install_requires=open('requirements.txt').read().splitlines(),
    long_description=long_description,
    long_description_content_type='text/markdown'
)
