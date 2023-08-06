import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

requirements = [
    'numpy',
    'scikit-learn',
    'dlib',
    'face_recognition',
]

setuptools.setup(
    name='FaceFlow',
    version='0.1.4',
    author='Jaewook Lee',
    author_email='me@jwlee.xyz',
    description='Face Classification package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/asheswook/FaceFlow',
    project_urls={
        'Bug Tracker': 'https://github.com/asheswook/FaceFlow/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package=setuptools.find_packages(),
    python_requires='>=3.9',
    install_requires=requirements,
)
