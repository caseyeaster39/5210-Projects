import project_utils
import robot_class


def main():                                                                         # Main function
    robot = robot_class.Robot(1000, protocol='random', layout='a')                  # Initialize robot

    robot.start_procedure()                                                         # Run episodes

    project_utils.report_printout(robot)                                            # Print results
    project_utils.display_results(robot)                                            # Display paths


if __name__ == '__main__':                                                          # Python best practices
    main()
