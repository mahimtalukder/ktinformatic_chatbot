#dataset Create
openai tools fine_tunes.prepare_data -f dataser.json

#Fine tune create
openai api fine_tunes.create -t dataser_prepared.jsonl -m adda