from setuptools import setup, find_packages

# from os.path import join, dirname

# try:
#     with open(join(dirname(__file__), "readme.md")) as fh:
#         long_description = fh.read()
# except:
#     long_description = (
#         ""
#     )

setup(
    name="dmte_lib",
    packages=find_packages(),
    version="0.0.0a0",
    license="MIT",
    description=("dmte"),
    author="dmatryus",
    author_email="dmatryus.sqrt49@yandex.ru",
    # long_description=long_description,
#     # long_description_content_type="text/markdown",
    url="https://gitlab.com/dmatryus.sqrt49/dmte",
    keywords=["TEXT_EDITOR"],
    install_requires=["Pygments"],
)