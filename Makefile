.PHONY : all

all :

install : all
	pip install -U .

package :
	python setup.py sdist

release : clean package
	twine upload dist/*

clean :
	rm -rf build dist mod_wsgi_httpd.egg-info

realclean : clean
	rm -f *.tar.gz
