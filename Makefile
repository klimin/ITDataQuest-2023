build:
	docker build -t danquest/danquest2023 .

run:
	docker run -d -p 2023:2023 -v data:/home/danquest2023/data --rm --name DanQuest2023 danquest/danquest2023

stop:
	docker stop DanQuest2023