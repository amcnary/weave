# Weave Grid coding exercise

## Run instructions

### Local
`python main.py [root directory] [port]`

### Docker
`./run.sh [root directory] [port]`

By default, this uses the current directory as default and runs on port 8000. Haven't implemented tying the two args to flags (--root [root] --port [port]), but this allows for some basic flexibility.

## Assumptions

*		This assumes that Docker is installed. I used
`Docker version 19.03.8, build afacb8b` but anything recent should work. No promises for older versions.

*		I used Python 2.7 if only because I haven't programmed on this laptop for a while and haven't gone through the work of upgrading to Python 3. Happy to rewrite in Python 3 if that's so desired.

*		I assume that we won't need to worry about pagination for the get request.

*		I don't support parent paths (..) for the API, which seems like the right security call. You can still init the server with a parent path, that just becomes the root node.

## Testing instructions
`python -m pytest`

I wrote some unit tests, but no integration/e2e tests, which didn't really seem necessary given the simplicity of the server. If we were writing a robust server, I'd def want to implement a healthz endpoint so we can monitor server health. I also should say that it's been a while since I've written python tests and they are much more annoying than TS (Jasmine) tests. Frontend is nice.

## TODO
I do want to implement the other endpoints, but it's late in the evening. If I get around to it this weekend, I may check in another change with them added. If I haven't done so, but you're looking for them, just let me know and I'll implement them more quickly.

I haven't used Swagger or Helm charts before, but I can read up on those and do those extra credit items if needed as well.