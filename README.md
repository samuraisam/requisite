#Requisite

Developing modern web applications often requires relying on a potentially very
large suite of 3rd party components. Dependency management for such applications
is a notorously agrivating experience.

In the python world we have some great tools such as 
[pip](http://www.pip-installer.org/en/latest/index.html),
[virtualenv](http://www.virtualenv.org/en/latest/) and 
[distribute](http://packages.python.org/distribute/),
that have allowed us to develop and share a wide breadth of software projects.

[PyPI](http://pypi.python.org) among various social coding sites are the preferred way
to distribute your project to a wider audience and for that they work great. However
when it's time to deploy your application to servers, depending on those would be a
a huge mistake. We've all done it, and sometimes the ramifications can be pretty painful.
Without knowing the uptime of PyPI or github, for example--it's not enough. Not
only that but the project could disappear, be moved or be changed in some way that
causes incompatability to your application.

Therefore it's a good idea to host your own packages somewhere. Like your own custom
installation of PyPI that has just the packages you need, at the versions you need
them, hosted in a place that won't change unless you say. Doesn't that sound complex?

It isn't!

Enter: [Chishop](https://github.com/benliles/chishop) (and of course it's evil cousin: 
[Requisite](https://github.com/samuraisam/requisite)!)

Chishop is a simplistic PyPI server written in Django just for this purpose. Requisite
is some opinionated glue code that utilizes pip and setuptools/distribute to acquire,
build and upload your packages to Chishop.

Here's how it works:

**1. Install Chishop [somewhere](http://ep.io)**

It's a Django project so this one is pretty simple. However you can follow a 
[guide](http://ssutch.org/chishop-epio) I have written to easily deploy to ep.io.

Ensure you add your Chishop credentials to your `~/.pypirc` file as these will be used
later on.

**2. Install Requisite**

		$ sudo pip install requisite

**3. Create a frozen pip requirements file**

You are already using using pip and `requirements.txt` right? Good. First generate a 
frozen pip requirements file:

		$ cd my_project
    $ pip freeze -r requirements.txt frozen-requirements.txt

**4. Upload to your Chishop repository**

    $ req requisite -r frozen-requirements.txt --repository=my_chishop --clean-cache

That's it. In your deploys you can use this new repository by specifying an 
`--index-url` [see here](http://www.pip-installer.org/en/latest/requirement-format.html)
at the top of your `frozen-requirements.txt` file. pip will then use that server to download
dependencies.

###A word to the wise
Do note that when using this method of dependency management, it's advisable that you
take reasonable security precautions. If you happen to be using Chishop and Requisite 
on ep.io, your data will be on the public internet. Be sure to **abstain from including
sensitive data** in your python packages. Chishop could also use some help implementing
a more secure mode of operation. Even then, be wary.
