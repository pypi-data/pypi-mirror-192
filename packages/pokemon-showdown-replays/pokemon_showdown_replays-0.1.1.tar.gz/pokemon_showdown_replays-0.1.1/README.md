# Pokémon Showdown! Replays
## Usage
To create a replay you will need a log file produced by a [Pokémon Showdown!](https://github.com/smogon/pokemon-showdown) server.
### Installation
```sh
pip install pokemon_showdown_replays
```
### Creating [replay.pokemonshowdown.com](https://replay.pokemonshowdown.com) replays
```python
from pokemon_showdown_replays import Replay, Upload

replay_object = Replay.create_replay_object(log, show_full_damage = False, client_location = "https://play.pokemonshowdown.com)
html = Upload.create_replay(replay_object)
```
### Creating [play.pokemonshowdown.com](https://play.pokemonshowdown.com) download replays
```python
from pokemon_showdown_replays import Replay, Download

replay_object = Replay.create_replay_object(log, show_full_damage = False, replay_embed_location = "https://play.pokemonshowdown.com/js/replay-embed.js")
html = Download.create_replay(replay_object)
```
The `show_full_damage` parameter is optional and defaults to `False`. When it is `True` and the log produced by the Pokémon Showdown! server has health shown in
full (ie. 347/550 and not 64/100), the replay will show the exact damage dealt by a move and the exact percentage of health a pokemon has left.
For example:
347 / 550 will be shown as 63.1% hp when it is enabled and 64% hp when it is disabled. It will also be 64/100 in the replay's log.
`replay_embed_location` can be used to show pokemon that do not exist on play.pokemonshowdown.com in a replay. This works by using the replay embed from the custom
[client](https://github.com/smogon/pokemon-showdown-client) in which the pokemon has a sprite, allowing it to be shown in the replay.
`client_location` works in the same way but uses the whole client instead of just the replay embed.