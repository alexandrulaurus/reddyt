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

`TODO: add indexes for mongodb`

### server
Starts a flask server and displays a welcome message

`TODO: expose search endpoint`
