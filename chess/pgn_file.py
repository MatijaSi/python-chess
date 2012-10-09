import chess
import re

class PgnFile(object):
    def __init__(self):
        self._games = []

    def add_game(self, game):
        self._games.append(game)

    def __len__(self):
        return len(self._games)

    def __getitem__(self, key):
        return self._games[key]

    def __setitem__(self, key, value):
        self._games[key] = value

    def __delitem__(self, key):
        del self._games[key]

    def __iter__(self):
        for game in self._games:
            yield game

    def __reversed__(self):
        for game in reversed(self._games):
            yield game

    def __contains__(self, game):
        return game in self._games

    @classmethod
    def open(cls, path):
        tag_regex = re.compile("\\[([A-Za-z0-9]+)\\s+\"(.*)\"\\]")

        pgn_file = PgnFile()
        current_game = None
        in_tags = False

        for line in open(path, 'r'):
            # Decode and strip the line.
            line = line.decode('latin-1').strip()

            # Skip empty lines and comments.
            if not line or line.startswith("%"):
                continue

            # Check for tag lines.
            tag_match = tag_regex.match(line)
            if tag_match:
                tag_name = tag_match.group(1)
                tag_value = tag_match.group(2).replace("\\\\", "\\").replace("\\[", "]").replace("\\\"", "\"")
                if current_game:
                    if in_tags:
                        current_game.set_header(tag_name, tag_value)
                    else:
                        pgn_file.add_game(current_game)
                        current_game = None
                if not current_game:
                    current_game = chess.Game()
                    current_game.set_header(tag_name, tag_value)
                in_tags = True
            # Parse movetext lines.
            else:
                if current_game:
                    # TODO: Parse the actual movetext.
                    pass
                else:
                    raise PgnError("Invalid PGN. Expected header before movetext: %s", repr(line))
                in_tags = False

        if current_game:
            pgn_file.add_game(current_game)

        return pgn_file
