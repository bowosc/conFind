**Note: I am ashamed of some of the far-from-best practices used in this code. Were I coding this today, it would look different.**


ConstAnt is a near-finished project centered around the idea of a search engine that enables a user to search a mathematical expression by the result, kind of like a reverse calculator.

The data, thousands of numbers (constants), is initially generated by a script that's run by the site on boot. From here, users have the ability to post (and name) their own constants, making sure any gaps in the set are filled. Users can also like and comment under other's constants, with an algorithm hiding less-common constants while those more likely to be useful float to the top.

ConstAnt uses a Python backend with a lot of SQLAlchemy ORM, running on a Flask site. A lot of the work here is in the data-gen and searching algorithms.
