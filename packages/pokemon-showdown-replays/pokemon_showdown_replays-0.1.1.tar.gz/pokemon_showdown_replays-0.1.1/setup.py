# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pokemon_showdown_replays']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pokemon-showdown-replays',
    'version': '0.1.1',
    'description': 'A package for generating pokemon showdown replays from pokemon showdown logs',
    'long_description': '# Pokémon Showdown! Replays\n## Usage\nTo create a replay you will need a log file produced by a [Pokémon Showdown!](https://github.com/smogon/pokemon-showdown) server.\n### Installation\n```sh\npip install pokemon_showdown_replays\n```\n### Creating [replay.pokemonshowdown.com](https://replay.pokemonshowdown.com) replays\n```python\nfrom pokemon_showdown_replays import Replay, Upload\n\nreplay_object = Replay.create_replay_object(log, show_full_damage = False, client_location = "https://play.pokemonshowdown.com)\nhtml = Upload.create_replay(replay_object)\n```\n### Creating [play.pokemonshowdown.com](https://play.pokemonshowdown.com) download replays\n```python\nfrom pokemon_showdown_replays import Replay, Download\n\nreplay_object = Replay.create_replay_object(log, show_full_damage = False, replay_embed_location = "https://play.pokemonshowdown.com/js/replay-embed.js")\nhtml = Download.create_replay(replay_object)\n```\nThe `show_full_damage` parameter is optional and defaults to `False`. When it is `True` and the log produced by the Pokémon Showdown! server has health shown in\nfull (ie. 347/550 and not 64/100), the replay will show the exact damage dealt by a move and the exact percentage of health a pokemon has left.\nFor example:\n347 / 550 will be shown as 63.1% hp when it is enabled and 64% hp when it is disabled. It will also be 64/100 in the replay\'s log.\n`replay_embed_location` can be used to show pokemon that do not exist on play.pokemonshowdown.com in a replay. This works by using the replay embed from the custom\n[client](https://github.com/smogon/pokemon-showdown-client) in which the pokemon has a sprite, allowing it to be shown in the replay.\n`client_location` works in the same way but uses the whole client instead of just the replay embed.',
    'author': 'eyalmen',
    'author_email': 'dave.eyal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
