There's no way to modify the visibility of your posts to "Only me" in bulk. It has to be a tedious task of individually going through each one of them.

This script attempts to solve that problem. You have to intercept authenticated post requests to steal the cookies and other values. Aside from that, you have to leverage the Graph API to get the post ids.