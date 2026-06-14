convert:
	python scripts/convert.py -i playlists.json -o /tmp/playlists.json
	-diff --color=always playlists.json /tmp/playlists.json
	mv -i /tmp/playlists.json playlists.json
