
GIT_PORCELAIN_STATUS=$(shell git status --porcelain)
CURRENT_BRANCH=$(shell git branch | grep "*" | sed -r "s/.\s(.*)/\1/g")

nothing:
	echo '0'
create-images-and-readme:
	python create_images_and_readme.py
upload-images:
	mkdir -p tmp
	rm -Rf tmp/*
	cp *.png tmp
	if [ -n "$(GIT_PORCELAIN_STATUS)" ]; \
	then \
	    echo 'YOU HAVE UNCOMMITED CHANGES'; \
	    git status; \
	    exit 1; \
	fi
	git checkout gh-pages
	cp tmp/*.png .
	git add *.png
	git commit --amend -m "gh-pages images"
	git checkout $(CURRENT_BRANCH)
	echo "Now:"
	echo "git push -f origin gh-pages"
	echo "git add README; git commit -m ...; git push origin master"
