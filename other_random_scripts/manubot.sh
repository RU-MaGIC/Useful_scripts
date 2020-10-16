#!/bin/bash
# Just a little script to make it easier to set up a manubot repo since I got sick of typing in all the commands

# Personal account set up
source ./.git_token # grab the github token info from a file
cd Github #just where I put this all on my machine- so creative

read -p "Enter the owner: " OWNER
read -p "Enter the repo name: " REPO

echo $TOKEN
curl -H "Authorization: token $TOKEN" https://api.github.com/user/repos -d "{\"name\":\"$REPO\"}"

# The manubot steps, from the manubot rootstock instructions
git clone --single-branch https://github.com/manubot/rootstock.git $REPO
cd $REPO
git remote add rootstock https://github.com/manubot/rootstock.git
git remote set-url origin https://github.com/$OWNER/$REPO.git
git push --set-upstream origin master
sed "s/manubot\/rootstock/$OWNER\/$REPO/g" README.md > tmp && mv -f tmp README.md
sed "s/manubot\.github\.io\/rootstock/$OWNER\.github\.io\/$REPO/g" README.md > tmp && mv -f tmp README.md
git rm .travis.yml
git rm .appveyor.yml
git rm ci/install.sh
git rm content/02.delete-me.md
git add --update
git commit --message "Brand repo to $OWNER/$REPO"
git push origin master

cd ~
rm -rf Github/$REPO

echo "Now go to your Github account, make sure you add the Github pages to the gh-pages branch."
