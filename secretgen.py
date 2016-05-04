import base64
import os
import sys
import yaml
import re
import time


def generatesecret(secretname,filelist):
    secretdict = dict(
        apiVersion = 'v1',
        kind = 'Secret',
        type = 'Opaque',
    )

    pattern = re.compile("\.?[a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*")
    secretdata = {}

    for currfile in filelist:
        print ("Processing {}".format(currfile))
        _, fname = os.path.split(currfile)
        if (pattern.match(fname)== None):
            print("%s is an invalid filename to be used as a secret key...exiting") % currfile
            sys.exit(30)
        with open(currfile) as f:
            encoded = base64.b64encode(f.read())
            secretdata[fname] = encoded

    metadata = {}
    annotations = {}
    annotations["create-date"] = time.strftime("%Y-%m-%d %H:%M:%S")
    annotations["built-by"] = "Automated secret builder"
    metadata['name']=secretname
    metadata['annotations'] = annotations
    secretdict['data']=secretdata
    secretdict['metadata']=metadata
    return yaml.dump(secretdict, default_flow_style=False)


def main():
    print generatesecret(sys.argv[1],sys.argv[2:])

if __name__ == '__main__':
    main()