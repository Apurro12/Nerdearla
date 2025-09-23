# And here?

In this the example there are multiples mcp servers
1) One to analize jpg images
2) One to interact with github
3) One to interact with databases

One can deploy different servers in isolation and check the different tools, some use cases could be

1) Analize some data from a given image
2) Ask the llm to fix some github issue
3) Ask to extract some data from the databases (this is our original example)

As exercise you could figure out hoy to connect to multiples mcp servers at the same time (help: you can use AsyncExitStack from contextlib to initiatiate all the sessions at the same time)