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
                'drive_robot = dev_robot.robot_driving.cmd_vel_robot_drive:main',
                'pub_imu = dev_robot.sensor_data_publisher.imu_publisher:main',
                'pub_encoders = dev_robot.sensor_data_publisher.encoders_pub:main',
                'pub_camera = dev_robot.sensor_data_publisher.image_pub:main',
                'odometery = dev_robot.odom.odometery:main',

        ],
    },
)
