from setuptools import setup, find_packages

# # reading long description from file
# with open('DESCRIPTION.txt') as file:
long_description = "test"


# # specify requirements of your package here
REQUIREMENTS = ['requests']

# some more details
CLASSIFIERS = [
	'Development Status :: 4 - Beta',
	'Intended Audience :: Developers',
	'Topic :: Internet',
	'License :: OSI Approved :: Apache Software License',
	'Programming Language :: Python',
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.6',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
	]

# calling the setup function
setup(name='CoreIndicators',
	version='1.0.1',
	description='Strategy to generate buy and sell signals for stocks',
	long_description=long_description,
	url='https://github.com/red9811/CoreIndicators',
	author='TraderNag',
	author_email='reachnag77@gmail.com',
	license='Apache',
	packages=find_packages(),
	classifiers=CLASSIFIERS,
	install_requires=REQUIREMENTS,
	keywords='Trend signals buy sell'
	)
