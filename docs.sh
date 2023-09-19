cd docs
sphinx-quickstart
make html
cd ..
sphinx-apidoc -o docs aiofauna --separate 
cd docs
make html
cd ..
