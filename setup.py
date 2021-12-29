#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-storynory.jarbasai=skill_storynory:StoryNorySkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-storynory',
    version='0.0.1',
    description='ovos storynory skill plugin',
    url='https://github.com/JarbasSkills/skill-storynory',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_storynory": ""},
    package_data={'skill_storynory': ['locale/*', 'res/*', 'ui/*']},
    packages=['skill_storynory'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
