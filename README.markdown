Whiskey - An minimal Python WSGI web framework
===============================================

After nosing round various micro and minimal frameworks, I thought I'd write my own for managing small / medium scale apps with varying roles, from services, to full sites, to google app engine sites.

I've tried to combine elements (shamelessly copied some) from an number of small WSGI frameworks like: [Paste][paste], [Juno][juno], [Web.py][webpy], [Newf][newf], [Itty][itty] and [Werkzeug][werkzeug].

Core Philosophy
---------------

Whiskey's core philosophy is that its simple and components are switchable, I want a certain level of "plumbing" taken care of for me, but I also want to be able to define my own rules.  So with that in mind Whiskey, aims to provide examples of flexible application level routing, which are easy to use or even easier to define your own.

TODO
----

* Lots - test and refactor
* More examples
* Improved handling of WSGIErrors - it has a smell at the moment.
* Decorator based routing - its simple!
* Mixed routing, With class based handlers for routes and reversing of routes.
* Support for middleware? Request and response
* Production WSGI interface for Apache

[itty]: http://github.com/toastdriven/itty/tree/master
[juno]: http://github.com/breily/juno/tree
[webpy]: http://webpy.org/
[newf]: http://github.com/JaredKuolt/newf/tree
[paste]: http://pythonpaste.org/
[werkzeug]: http://werkzeug.pocco.org/