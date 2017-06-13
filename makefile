
.PHONY: init
init:
	mkdir /tmp/scripts
	echo "#!/usr/bin/bash" >> /tmp/scripts/hello
	echo "echo hello" >> /tmp/scripts/hello
	chmod +x /tmp/scripts/hello
clean:
	rm -rf /tmp/scripts

