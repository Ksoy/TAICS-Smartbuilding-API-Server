## Install

`pip install -r requirements.txt`

## Configuration

1. Create `.env` file from sample

	`cp .env.sample .env`

2. Edit `.env` to meet the requirements

	- Set `HOST` to the address you want to serve, default `0.0.0.0` works for all addresses
	- Set `PORT` to the port you want to serve, default `80`
	- Set the Flask secret "SECRET_KEY" to any string you like, a random string that is hard to guess is recommended
	- Set `DEBUG` to `True` if you want to modify, develop and debug the code, default `False`

## Start

`python -m subsystem`
