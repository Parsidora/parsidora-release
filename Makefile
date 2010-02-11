VERSION=$(shell awk '/Version/ { print $$2 }' parsidora-release.spec)

CVSROOT = $(shell cat CVS/Root 2>/dev/null || :)

CVSTAG = V$(subst .,-,$(VERSION))

all:

tag-archive:
	@cvs -Q tag -F $(CVSTAG)

create-archive:
	@rm -rf /tmp/fedora-release
	@cd /tmp ; cvs -Q -d $(CVSROOT) export -r$(CVSTAG) parsidora-release || echo "Um... export aborted."
	@mv /tmp/parsidora-release /tmp/parsidora-release-$(VERSION)
	@cd /tmp ; tar -czSpf parsidora-release-$(VERSION).tar.gz parsidora-release-$(VERSION)
	@rm -rf /tmp/parsidora-release-$(VERSION)
	@cp /tmp/parsidora-release-$(VERSION).tar.gz .
	@rm -f /tmp/parsidora-release-$(VERSION).tar.gz
	@echo ""
	@echo "The final archive is in parsidora-release-$(VERSION).tar.gz"

archive: tag-archive create-archive
