""" Setup file for custom Gym environments (PIP package )"""

from setuptools import setup, find_packages


# with open(
#         "../../../Git code/widowx_paperwithcode/widowx_paperwithcode/b4_REPRODUCIBLE REINFORCEMENT LEARNING/b4_rl_reach-master/rl_reach-master/code/gym_envs/README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setup(
    name="gym_envs",
    version="0.1.0",
    author="xxxxx",
    description="Gym environments for RL reaching tasks",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    download_url='https://pypi.org/project/elastictools/',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
    keywords=["Reinforcement_Learning", "OpenAI_Gym"],
    install_requires=["gym", "numpy", "pybullet"]
)
