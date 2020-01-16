import setuptools

with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
        name="sp_licitacoesPy", # Replace with your own username
        version="0.0.1",
        author="PzanettiD",
        author_email="zanetti.pepe@gmail.com",
        description="Python3 Wrapper para API de licitações da Prefeitura de São Paulo",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/PzanettiD/sp_licitacoesPy",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
)
