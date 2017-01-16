# reddyt
A reddit search engine written in Python

## Modules
### indexer
Starts a reddit client, fetches items from subreddits and persists items into mongodb

#### Configuration
One can define a list of subreddits along with several additional settings to
process that subreddit:

```
{
    "subreddits" : [
        {
            "name"              : "analog",
            "initial_dump"      : 200,
            "refresh_limit"     : 25,
            "refresh_interval"  : 60
        },
        {
            "name"              : "redditdev",
            "initial_dump"      : 200,
            "refresh_limit"     : 30,
            "refresh_interval"  : 30
        },
        {
            "name"              : "jailbreak",
            "initial_dump"      : 100,
            "refresh_limit"     : 25,
            "refresh_interval"  : 10
        }
    ]
}
```

* `name` : name of the subreddit to be processed
* `initial_dump` : 
  - this value represents the number of submissions to be fetched when the application starts
  - reddit client used fetches a maximum of 1000 which is the limit of most subreddits
* `refresh_limit` : 
  - represents the number of items to be fetched after the initial dump, after a certain amount of time; think about a lookback range for the posts you want to update
* `refresh_interval` :
  - specifies the time interval at which the underlying subreddit is going to be processed again

This definition should be set in the `config.json` file which gets picked up when the application starts.


### server
Exposes the following endpoints at `localhost:5000`

#### `/items?subreddit=<subreddit>&from=<from>&to=<to>[&keyword=<keyword>]`
Returns a list of items formatted as JSON based on the given parameters
* method: `GET`
* content-type: `application/json`
* params:
  - query:
    - `subreddit`: 
      - mandatory
      - name of the subreddit to search content
    - `from`:
      - mandatory
      - POSIX timestamp for the lower limit of the content based on `created_utc` time from Reddit API
    - `to`:
      - mandatory
      - POSIX timestamp for the upper limit of the content based on `created_utc` time from Reddit API
    - `keyword`:
      - optional
      - word to search in item content
* output example:
```
mybook:~ alexandru$ curl -i "http://localhost:5000/items?subreddit=jailbreak&from=1483309088&to=1484526822&keyword=new"
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 890
Server: Werkzeug/0.11.15 Python/2.7.13
Date: Mon, 16 Jan 2017 01:10:48 GMT

[
    {
        "body": "its not recommended on the latest because cokepokes doesn't know what the new security features it has in it. But I am on 9.45.3. the latest is 9.45.10, but he recommends not updating to that one. 9.45.3 works perfectly fine for me",
        "created": 1484526695,
        "id": "dch6z4n"
    },
    {
        "body": "1 word \"stay\", but maybe its hard not to upgrade because latest ios got some new features.\nBut it wont be as stable as ios 8 jailbreak.\n\nHmm. I know you confused bout this",
        "created": 1484526595,
        "id": "dch6w2y"
    },
    {
        "body": "Well that's taking it to a new level ",
        "created": 1484526103,
        "id": "dch6gl7"
    },
    {
        "created": 1484524404,
        "id": "5o7d46",
        "title": "[Request] Simple tweak to make Safari 'Request Desktop Site' to open in a new tab"
    }
]
```

## How to run

### Prerequisites:

* docker >= 1.12.6
* docker-compose >= 1.9.0

Make sure you are in the root directory and run the following command

```
docker-compose -f reddyt-compose.yml up
```

## TODO

`TODO: unit tests`
