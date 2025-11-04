#!/usr/bin/env python3
import rospy
import time
from clover import srv
from std_srvs.srv import Trigger

# Inicializa o nó ROS
rospy.init_node('takeoff_land_example')

# Conecta aos serviços do Clover
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)
arming = rospy.ServiceProxy('mavros/cmd/arming', srv.SetBool)

# Aguarda os serviços estarem disponíveis
rospy.wait_for_service('navigate')
rospy.wait_for_service('land')

print("Arming motors...")
arming(True)
rospy.sleep(2)

# Subida gradual (0 → 2 m em ~10 s)
print("Taking off slowly...")
for i in range(0, 21):
    height = i * 0.1  # sobe 0.1 m a cada 0.5 s
    navigate(x=0, y=0, z=height, yaw=float('nan'), speed=0.2, frame_id='body', auto_arm=True)
    rospy.sleep(0.5)

print("Hovering for 10 seconds...")
rospy.sleep(10)

# Descida gradual
print("Landing slowly...")
for i in range(20, -1, -1):
    height = i * 0.1
    navigate(x=0, y=0, z=height, yaw=float('nan'), speed=0.2, frame_id='body')
    rospy.sleep(0.5)

print("Disarming...")
land()
arming(False)
print("Mission completed.")
