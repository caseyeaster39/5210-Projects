from agent import Agent


def main():
    # Question 6, running for n=100 orders
    n = 100
    consecutive_agent = Agent()                             # Initialize agent
    for i in range(n):                                      # 100 orders
        consecutive_agent.protocol()                        # Run protocol

    # Question 5
    edge_case_agent = Agent()                               # Initialize agent
    edge_case_agent.protocol(rand=False, shelves=[33],      # Passing in our own parameters for edge case
                             div=6, single_run=True)


if __name__ == '__main__':
    main()
