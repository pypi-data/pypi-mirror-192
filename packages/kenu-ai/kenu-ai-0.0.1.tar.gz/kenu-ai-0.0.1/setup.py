from setuptools import setup

setup(
	name="kenu-ai",
	version="0.0.1",
	description="Python Chat AI",
	author="r4isy",
	author_email="r4isy@kenucheck.xyz",
	packages=["kenu-ai"],
	install_requires=[
	'googletrans==4.0.0-rc1',
	'requests'
	]
	)