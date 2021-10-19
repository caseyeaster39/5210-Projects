from agent import Agent


def main():
    # Question 6
    n = 100
    consecutive_agent = Agent()
    for i in range(n):
        consecutive_agent.protocol()

    # Question 5
    edge_case_agent = Agent()
    edge_case_agent.protocol(rand=False, shelves=[33],
                             div=6, printouts=True)


if __name__ == '__main__':
    main()
