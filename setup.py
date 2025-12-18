import os
import setuptools


def get_requirements():
    """Return requirements from requirements.txt, excluding editable installs (-e / --editable) and comments."""
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    requirements = []
    with open(req_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # skip editable installs
            if line.startswith('-e') or line.startswith('--editable'):
                continue
            requirements.append(line)


setuptools.setup(
    name="NetworkSecurity",
    version="0.0.1",
    description="NetworkSecurity",
    author="Sapana Dhami",
    packages=setuptools.find_packages(),
    install_requires= get_requirements(),
)