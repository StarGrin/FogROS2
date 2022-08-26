from launch_ros.actions import Node
import fogros2

class myCloudInstance(fogros2.AWSCloudInstance):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def pip_install_interface(self):
        print("installing opencv")

        # opencv-python: 只包含opencv库的主要模块. 一般不推荐安装.
        # opencv-contrib-python: 包含主要模块和contrib模块, 功能基本完整, 推荐安装.
        # opencv-python-headless: 和opencv-python一样, 但是没有GUI功能, 无外设系统可用.
        # opencv-contrib-python-headless: 和opencv-contrib-python一样但是没有GUI功能. 无外设系统可用.

        self.pip_install("opencv-python-headless")


def generate_launch_description():
    ld = fogros2.FogROSLaunchDescription()
    machine1 = myCloudInstance(
        region="us-west-1", 
        ec2_instance_type="t2.micro", 
        ami_image=ami_image()
    )

    talker_node = Node(
        package="video_transp", 
        executable="video_pub", 
        output="screen"
    )

    listener_node = fogros2.CloudNode(
        package="video_transp",
        executable="video_sub",
        output="screen",
        machine=machine1,
    )
    ld.add_action(talker_node)
    ld.add_action(listener_node)
    return ld


def ami_image():
    # An AMI is an Amazon Web Services virtual machine image with a
    # pre-installed OS and dependencies.  We match the AMI in the
    # cloud to have the same OS release as the robot.  Currently we
    # support Ubuntu 20.04 and 22.04.

    import lsb_release

    ubuntu_release = lsb_release.get_os_release()["RELEASE"]

    if ubuntu_release == "20.04":
        return "ami-00f25057ddc9b310b"
    if ubuntu_release == "22.04":
        return "ami-0b6030c78f8b2f076"

    raise ValueError(f"No AMI for {ubuntu_release}")
