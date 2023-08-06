from setuptools import setup, find_packages

# # reading long description from file
# with open('DESCRIPTION.txt') as file:
long_description = "Buy and sell signals for stocks"


# # specify requirements of your package here
#need python 3.8 or higher
REQUIREMENTS  = ['python>=3.8']
# some more details
CLASSIFIERS = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Developers',
	'Topic :: Internet',
	'License :: OSI Approved :: Apache Software License',
	'Programming Language :: Python',
	'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
	]

# calling the setup function
setup(name='CoreIndicators',
	version='1.0.5',
	description='Strategy to generate buy and sell signals for stocks',
	long_description=long_description,
	url='https://github.com/red9811/CoreIndicators',
	author='TraderNag',
	author_email='reachnag77@gmail.com',
	license='Apache',
	packages=['TrendSignalIndicator'] ,#find_packages(),
	classifiers=CLASSIFIERS,
	install_requires=REQUIREMENTS,
	keywords='Trend signals buy sell'
	)
