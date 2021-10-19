from agent import Agent
# TODO: comments, edge cases, multiple orders


def main():
    # Question 5
    edge_case_agent = Agent()
    edge_case_agent.protocol(rand=False, shelves=[33], div=6, printouts=True)

    # TODO: Fix this:
    edge_case_agent.protocol(rand=False, shelves=[5], div=15, printouts=True)

    # n = 100
    # consecutive_agent = Agent()
    # for i in range(n):
    #     consecutive_agent.protocol()


if __name__ == '__main__':
    main()
