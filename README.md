# reddyt
A reddit search engine written in Python

## Modules
### indexer
Starts a reddit client, fetches itmes from subreddits and persists items into mongodb

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

#### `/`
Displays a welcome message
* method: `GET`
* params: none

#### `/items?subreddit=<subreddit>&from=<from>&to=<to>[&keyword=<keyword>]`
Returns a list of items formatted as JSON based on the given parameters
* method: `GET`
* params:
  - query:
    - `subreddit`: 
      - mandatory
      - name of the subreddit to search content
    - `from`:
      - mandatory
      - POSIX timestamp for the lower limit of the content `created_utc` time from Reddit API
    - `to`:
      - mandatory
      - POSIX timestamp for the upper limit of the content based on `created_utc` time from Reddit API
    - `keyword`:
      - optional
      - word to search in item content
* content-type: `application/json`

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
