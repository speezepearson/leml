all:
	for f in demo-source.*; do make $${f/#demo-source/demo-compiled}; done

demo-compiled.%: demo-source.%
	python -m markup -f $* modules.json < $^ > $@