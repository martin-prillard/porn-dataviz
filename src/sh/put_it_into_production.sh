#!/bin/bash

# Launch it from gh-pages branch

# Development environment to production : 
# to copy master files on the online website (gh-pages branch)

# dataset
git checkout master -- dataset/generated/
# html
git checkout master -- index.html
git checkout master -- html/
# js
git checkout master -- javascripts/
# css
git checkout master -- stylesheets/