APPNAME = SepulnationTV
VERSION = 2.0.0
ROKU_DEV_TARGET ?= 192.168.1.100

.PHONY: build install clean

build:
	@echo "Building $(APPNAME) v$(VERSION)..."
	@cd .. && zip -r roku/$(APPNAME).zip roku/manifest roku/source roku/components roku/images -x "roku/Makefile" "roku/*.zip"
	@echo "Build complete: $(APPNAME).zip"

install: build
	@echo "Installing on Roku at $(ROKU_DEV_TARGET)..."
	@curl --user rokudev:$${DEVPASSWORD} --digest -F "mysubmit=Install" -F "archive=@$(APPNAME).zip" http://$(ROKU_DEV_TARGET)/plugin_install
	@echo "Install complete!"

clean:
	@rm -f $(APPNAME).zip
	@echo "Cleaned."
