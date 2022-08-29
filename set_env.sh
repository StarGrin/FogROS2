export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file://$(pwd)/install/fogros2/share/fogros2/configs/cyclonedds.ubuntu.$ver.xml

echo $RMW_IMPLEMENTATION
echo $CYCLONEDDS_URI