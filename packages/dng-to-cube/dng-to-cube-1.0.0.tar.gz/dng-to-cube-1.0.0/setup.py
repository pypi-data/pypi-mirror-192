from setuptools import setup

setup(
    name='dng-to-cube',
    version='1.0.0',
    description='Convert DNG files to LUT cube files',
    py_modules=['dng_to_cube'],
    entry_points={
        'console_scripts': [
            'dng-to-cube=dng_to_cube:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    keywords='dng cube lut conversion',
    author='Felix Furtado',
    author_email='felixfurtado809@gmail.com',
    license='MIT'
)
