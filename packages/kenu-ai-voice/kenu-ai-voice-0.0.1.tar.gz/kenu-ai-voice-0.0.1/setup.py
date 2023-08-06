from setuptools import setup

setup(
	name="kenu-ai-voice",
	version="0.0.1",
	description="Python Voice Chat AI",
	author="r4isy",
	author_email="r4isy@kenucheck.xyz",
	packages=["kenu_ai_voice"],
	install_requires=[
	'gtts',
	'playsound==1.2.2',
	'speechrecognition',
	'googletrans==4.0.0-rc1',
	'requests',
	'kenu_ai'
	]
	)