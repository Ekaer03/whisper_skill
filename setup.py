"""Setup configuration for whisper_skill"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip()]

setup(
    name='whisper_skill',
    version='1.0.0',
    description='Audio transcription skill using OpenAI Whisper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ekaer03',
    url='https://github.com/Ekaer03/whisper_skill',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='whisper transcription audio speech-to-text',
)
