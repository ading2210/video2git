# Video to Github Contributions Graph

This is a script that can convert any video (that's less than 8000 frames) into commits on a user's contributions graph.

## Usage

1. Clone this repository.
2. Cd into the created directory.
3. Run `pip3 install -r requirements.txt` to install any dependencies.
4. Copy `sample_config.json` to `config.json`.
5. Fill out the relavent information.
6. Run `python3 main.py`.

Note: depending on how dark your video is, the conversion process will run at ~1-3 fps.

## Upcoming features

- Rendering captions in the remaining space
- Another script for screenshotting the generated graphs

## License

This repository is licenced under the GNU GPL v3.
