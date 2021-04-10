#!/usr/bin/env bash
DIR=dist

git checkout --orphan gh-pages
npm run build
git --work-tree $DIR add --all
git --work-tree $DIR commit -m "gh-pages"
git push origin HEAD:gh-pages --force
rm -rf $DIR
git checkout -f main 
git branch -D gh-pages
