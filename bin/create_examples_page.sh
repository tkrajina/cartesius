python example.py
tar -cvf examples.tar *png *html
rm *png *html
mv examples.tar /tmp/
git checkout gh-pages
mv /tmp/examples.tar .
tar -xvf examples.tar
rm *tar
git add *.png *.html
git commit --amend -m "Examples"
