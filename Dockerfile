ARG UBUNTU_DISTRO=jammy
ARG ROS_DISTRO=rolling
FROM ubuntu:${UBUNTU_DISTRO}

# Set up install, set tzdata
ARG UBUNTU_DISTRO
ARG ROS_DISTRO
# ENV TZ=America/Vancouver
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 添加国内apt源
RUN cp /etc/apt/sources.list /etc/apt/sources.list.backup && \
  echo 'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse\n\
  deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse\n\
  deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse\n\
  deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse\n'\
  > /etc/apt/sources.list

# Get ROS key
RUN apt update && apt install -y curl gnupg2 lsb-release && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Install apt deps 
# RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu ${UBUNTU_DISTRO} main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu ${UBUNTU_DISTRO} main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y \
  ros-${ROS_DISTRO}-desktop \
  ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
  iproute2 \
  net-tools \
  python3-colcon-common-extensions \
  python3-pip \
  unzip \
  wireguard
RUN rm -rf /var/lib/apt/lists/*

# Install AWS dep
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip && rm awscliv2.zip
RUN ./aws/install

# Install python deps
RUN python3 -m pip install --no-cache-dir -U boto3 paramiko scp wgconfig -i https://pypi.tuna.tsinghua.edu.cn/simple

# Create FogROS2 worspace and build it
ENV ROS_WS=/home/root/fog_ws
RUN mkdir -p ${ROS_WS}/src
WORKDIR ${ROS_WS}/src
COPY .  ${ROS_WS}/src/
WORKDIR ${ROS_WS}
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
      colcon build --cmake-clean-cache

# setup entrypoint
ENV ROS_DISTRO=${ROS_DISTRO}
COPY ./ros_entrypoint.sh /
RUN chmod +x /ros_entrypoint.sh

ENTRYPOINT [ "/ros_entrypoint.sh" ]
CMD ["bash"]
