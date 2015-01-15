#!/bin/bash

# Development environment to production : 
# to copy master files on this branch gh-pages (the online website)

# dataset
git checkout master -- dataset/generated/
# html
git checkout master -- index.html
git checkout master -- html/
# js
git checkout master -- javascripts/
# css
git checkout master -- stylesheets/
# README.md
git checkout master -- README.md
