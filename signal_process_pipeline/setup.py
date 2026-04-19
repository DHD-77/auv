from setuptools import find_packages, setup

package_name = 'signal_process_pipeline'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dhruv-h-dave',
    maintainer_email='dhruvhdave21@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publisher = signal_process_pipeline.publisher:main',
            'processor = signal_process_pipeline.processor:main',
            'output = signal_process_pipeline.output:main',
            'commander = signal_process_pipeline.commander:main',
            'navigator = signal_process_pipeline.navigator:main',
            'vision = signal_process_pipeline.vision_node:main',
        ],
    },
)
