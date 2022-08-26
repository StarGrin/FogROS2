from glob import glob
from setuptools import setup

package_name = 'video_transp'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, glob("launch/*.launch.py")),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='StarGrin',
    maintainer_email='1580842496@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "video_pub  = video_transp.pub_webcam:main",
            "video_sub  = video_transp.sub_webcam:main"
        ],
    },
)
