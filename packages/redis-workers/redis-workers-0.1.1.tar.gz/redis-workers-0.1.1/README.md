# redis-worker 🎉
A tool that simplifies Redis usage for repeating tasks

# Usage
`docker-compose up` to start Redis server

Give rd.cache() a key, callable and arguments.

````
    rd = redisWorker()

    games = rd.cache('games', db_app.get_table, 'games', ['game_id', 'appid'])
```