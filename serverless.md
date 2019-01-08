# Serverless tutorial

I got things to deploy to lambda on aws, but it is pretty annoying to do so. In comes serverless. This module makes things super easy to deploy to aws lambda and lots of other things, and includes a bunch of plugins that help make things even simpler.

[make dependency packages smaller plugin](https://github.com/dougmoscrop/serverless-plugin-include-dependencies)
[Python package manager plugin](https://www.npmjs.com/package/serverless-python-requirements)

```
sls plugin install -n serverless-python-requirements
```

I had a problem with my package being nearly 10 MB when compressed, which is almost the limit, so the depency smaller package may prove useful.

The python package manager plugin looks amazing. I would like to use this to automatically install all the dependencies of the python project, and also dockerize the python script before deploying it to lambda. Seems very promising since it seemed like docker may do a better job than lambda for what I need.