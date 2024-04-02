from setuptools import setup, find_packages

with open('VERSION', 'r') as version_file:
    version = version_file.read()

with open('LICENSE', 'r') as license_file:
    license = license_file.read()

with open('requirements.txt', 'r') as requirements_file:
    requirements = requirements_file.read().splitlines()

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

setup(name="SpotifyManager",
      version=version,
      description="A Spotify Manager",
      author="Noam Rotem",
      author_email="noamrooffical@gmail.com",
      long_description=readme,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      install_requires=requirements,
      license=license)
