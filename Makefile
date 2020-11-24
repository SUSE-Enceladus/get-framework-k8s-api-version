DESTDIR=
PREFIX=/usr
NAME=getkubectlversion
dirs = lib
files = Makefile README.md LICENSE get-framework-k8s-api-version setup.py requirements-dev.txt requirements.txt

verSpec = $(shell rpm -q --specfile --qf '%{VERSION}' *.spec)
verSrc = $(shell cat lib/getframeworkk8sapiversion/VERSION)

ifneq "$(verSpec)" "$(verSrc)"
$(error "Version mismatch, will not take any action")
endif

clean:
	@find . -name "*.pyc" | xargs rm -f
	@find . -name "__pycache__" | xargs rm -rf
	@find . -name "*.cache" | xargs rm -rf
	@find . -name "*.egg-info" | xargs rm -rf

pep8: clean
	@pep8 -v --statistics lib/getframeworkk8sapiversion/*
	@pep8 -v --statistics --ignore=E402 tests/*.py

tar: clean
	rm -rf $(NAME)-$(verSrc)
	mkdir $(NAME)-$(verSrc)

	cp -r $(dirs) $(files) "$(NAME)-$(verSrc)"
	tar -cjf "$(NAME)-$(verSrc).tar.bz2" "$(NAME)-$(verSrc)"
	rm -rf "$(NAME)-$(verSrc)"

test:
	py.test --no-cov-on-fail --cov=getframeworkk8sapiversion \
        --cov-report=term-missing --cov-fail-under=100 --cov-config .coveragerc
install:
	python3 setup.py install --prefix="$(PREFIX)" --root="$(DESTDIR)"
