import project_utils
import robot_class


def main():                                                                         # Main function
    # Edit number of episodes, 'random' or 'path' protocol, and layout 'a' or 'b'
    robot = robot_class.Robot(episodes=1000, protocol='random', layout='a')         # Initialize robot

    robot.start_procedure()                                                         # Run episodes

    project_utils.report_printout(robot)                                            # Print results


if __name__ == '__main__':                                                          # Python best practices
    main()
