#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# Resource & resource manager.
#
# yqm_leaf@163.com
#
# 07/14/19
#
# --------------------------------------------------------------------------

import re
import os

from shami.utils import list_file, get_cwd

class ResourceManager(object):

    def __init__(self):
        pass

    def list(self, full_path=False):
        """List all resources.
        :returns: None.
        """

        resource_dir = os.path.join(get_cwd(), 'resources')

        for i in list_file(resource_dir):
            yield i if full_path else os.path.basename(i)

    def lock(self, resource):
        """Lock a resource.
        :param    resource: a resource object.
        :returns: Status of locking a resource.
        """
        try:
            os.rename(resource.resource_file,
                      resource.resource_file + '.lck')
        except:
            return False

        return True

    def unlock(self, resource):
        """Unlock a resource.
        :param    resource: a resource object.
        :returns: Status of unlocking a resource.
        """
        try:
            os.rename(resource.resource_file + '.lck',
                      resource.resource_file)
        except:
            return False

        return True

    def acquire_resource(self, requirement):
        """Acquire resource.
        :params   requirement: dict of requirement.
        :returns: list of resource object(s) or None.
        """
        available_resources = []
        for k, v in requirement.items():
            for i in range(int(v)):
                r = self._acquire_resource(k)
                if not r:
                    return None
                else:
                    available_resources.append(r)
        return None if available_resources is [] else \
               available_resources

    def _acquire_resource(self, res_type):
        """Acquire a resource base on res_type.
        :params   string, resource type.
        :returns: resource object or None.
        """
        for device in self.list(full_path=True):
            if device.endswith('.lck'):
                continue
            r = Resource(device)
            if not r.res_type == res_type:
                continue
            if not self.lock(r):
                continue
            else:
                return r

        return None

    def release_resource(self, resources):
        """Release resources.
        :params   resources.  List of resource objects.
        :returns: status of releasing resources.
        """
        for r in resources:
            if not self.unlock(r): return False

        return True

class Resource(object):

    def __init__(self, resource_file):
        self.resource_file = resource_file
        pass

    def chrole(self, role):
        """
        Change role of a resource.
        :params role: role to be.
        """
        pass

    def health_chk(self):
        """
        Check health of a resource.
        """
        pass

    def show(self):
        """Show details of a resource.
        :returns: None."""
        with open(self.resource_file) as f:
            for line in f:
                # Skip comment lines.
                if re.search(" *#", line):
                    continue
                print(line)

    @property
    def res_type(self):
        """Resource type.
        :returns: string.  Resource type."""
        try:
            return self.parse()['res_type']
        except KeyError:
            return None

    def parse(self):
        """Parse a resource file.
        :returns: dict of a resource file."""
        d = {}
        with open(self.resource_file) as f:
            for line in f:
                # Skip comment lines.
                if re.search(" *#", line):
                    continue
                m = re.match(r"(\w+) *= *[\'\"]*([\.\w]+)", line, 
                        flags=re.IGNORECASE)
                if m:
                    k, v = m.group(1), m.group(2)
                    d[k] = v
        return None if d is {} else d
