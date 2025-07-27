#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

def send_goal(x, y, yaw=0.0, timeout=30.0):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = 0.0

    qx, qy, qz, qw = quaternion_from_euler(0.0, 0.0, yaw)
    goal.target_pose.pose.orientation.x = qx
    goal.target_pose.pose.orientation.y = qy
    goal.target_pose.pose.orientation.z = qz
    goal.target_pose.pose.orientation.w = qw

    rospy.loginfo("Sending goal: x=%.2f, y=%.2f, yaw=%.2f", x, y, yaw)
    client.send_goal(goal)
    finished = client.wait_for_result(rospy.Duration(timeout))

    if not finished:
        client.cancel_goal()
        rospy.logwarn("Timeout: Failed to reach (%.2f, %.2f)", x, y)
        return False
    elif client.get_state() != actionlib.GoalStatus.SUCCEEDED:
        rospy.logwarn("Move_base reported failure at (%.2f, %.2f)", x, y)
        return False
    return True

if __name__ == '__main__':
    rospy.init_node('waypoint_navigation')

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("Waiting for move_base action server...")
    client.wait_for_server()
    rospy.loginfo("Connected to move_base action server.")

    # Map of numbers to coordinates (as per your label)
    numbered_waypoints = {
        1: [1.296, -1.314],      # Rahim
        2: [-0.109, -1.242],     # Joshua
        3: [-1.532, -1.394],     # Yong Zhou
        4: [-1.817, -0.031],     # Daryl
        5: [-1.825, 1.787],      # Jarvis
        6: [-0.251, 1.628],      # Yong Jie
        7: [1.053, 1.670],       # Hazwan
        8: [1.251, 0.086],       # Kieran
        9: [0.086, 0.041]        # Middle
    }

    # Get 3 numbers from user input
    try:
        input_str = raw_input("Enter 3 waypoint numbers (1-9, space-separated): ")  # Python 2
    except NameError:
        input_str = input("Enter 3 waypoint numbers (1-9, space-separated): ")     # Python 3

    numbers = [int(n) for n in input_str.strip().split() if n.isdigit() and 1 <= int(n) <= 9]

    if len(numbers) != 3:
        rospy.logerr("Please enter exactly 3 valid numbers from 1 to 9.")
    else:
        for idx, n in enumerate(numbers):
            x, y = numbered_waypoints[n]
            success = send_goal(x, y, yaw=0.0, timeout=45.0)
            if success:
                rospy.loginfo("Reached position %d at (%.2f, %.2f)", n, x, y)
            else:
                rospy.logwarn("Skipped position %d at (%.2f, %.2f)", n, x, y)

