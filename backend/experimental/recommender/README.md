## Sketch Ideas for Recommender System


### Cold-start

At the beginning of the app, there are no data for training a recommender system. As a result, a fixed template for cold start is neccessary. However, it may be too "strict" for some users. 

Propose: Applying clustering method based on video's categories or what we already have, such as, objects in videos. After training, there will be `k` clusters that are ready to go. We will do like this, but keep in mind that, users will only see a strict number of results. The steps are as follows: 

Assume we allow users to see `z` samples from our `x` collection. 

1. We retrieve a `a` portion from `k` as it is the most related to user's first touch videos. 
and retrieve `b` portion from the remain. 
2. Selecting `z` and present it to users, the `z` will be re-selected each time users reload the page. 
### Right Moment

#### Implicit Information


#### Explicit Information