
.PHONY: init
init:
	mkdir /tmp/scripts
	echo "#!/usr/bin/bash" >> /tmp/scripts/hello
	echo "echo hello" >> /tmp/scripts/hello
	chmod +x /tmp/scripts/hello
	mkdir -p /tmp/jobs/1
	echo "#!/usr/bin/bash" >> /tmp/jobs/1/hello
	echo "echo hello every minute" >> /tmp/jobs/1/hello
	chmod +x /tmp/jobs/1/hello
clean:
	rm -rf /tmp/scripts
	rm -rf /tmp/jobs

