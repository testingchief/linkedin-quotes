![Build](http://img.shields.io/badge/release-1.0-GREEN.svg)
![Twitter](http://img.shields.io/badge/@testingchief--lightgrey?logo=twitter&amp;style=social)

# linkedin-quotes
Get a clean screenshot of any LinkedIn post to share them on Social Media.

![Auto Generated Image](https://github.com/testingchief/linkedin-quotes/blob/main/images/sample_post.png?raw=true)

### What do you need?
Get the URN from 'Embed this post' code in LinkedIn posts.
Example:
```
<iframe src="https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7107451783974645760" 
        height="904" width="504" frameborder="0" 
        allowfullscreen="" title="Embedded post"></iframe>
``` 
Required URN code is urn:li:ugcPost:7107451783974645760

### How to run?
```
py .\scripts\linkedin-quotes.py "<URN code>" 

```