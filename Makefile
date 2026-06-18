convert:
	python scripts/convert.py -i playlists.json -o /tmp/playlists.json
	mv /tmp/playlists.json playlists.json
