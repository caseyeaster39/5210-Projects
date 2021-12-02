from game_board import play_game


def main():
    while True:
        player_starts = input("Would you like to go first? (y/n)\n").lower()
        if player_starts == 'n' or player_starts == 'y':
            break
    max_starts = player_starts == 'n'
    play_game(max_starts=max_starts)


# for scripting purposes
if __name__ == '__main__':
    main()
