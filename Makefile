.PHONY: test package build smoke

test:
	python3 -m unittest discover -s tests -v
	go run $$(find static/files -name welcome.go)

package:
	python3 scripts/package.py

build:
	docker build -f dynamic/Dockerfile -t cybericebox/test-exercises:local .

smoke:
	docker build -f dynamic/Dockerfile --target test-tools -t cib-test-exercises:tools .
	CIB_DEMO_IMAGE=cybericebox/test-exercises:local python3 scripts/smoke.py
