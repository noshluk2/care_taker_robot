from setuptools import find_packages, setup
from glob import glob
import os 

package_name = 'dev_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robot',
    maintainer_email='hiba.glory@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'cmdvel_sub = dev_robot.cmd_vel_sub:main',
                'imu_pub = dev_robot.imu_publisher:main',
                'encoder_pub = dev_robot.motor_encoders:main',
                'odometery = dev_robot.odometery:main',
        ],
    },
)
