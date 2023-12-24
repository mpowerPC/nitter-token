# nitter-token

A simple script to grab a guest token from the unofficial twitter api and store it in guest_accounts.json to be used
by the guest account branch of nitter.

To build and run nitter-token in Docker:
```
docker build --tag nitter-token .
docker run --rm -v $(pwd)/logs:/src/logs -v {path to nitter folder}:/src/output --name nitter-token nitter-token
```