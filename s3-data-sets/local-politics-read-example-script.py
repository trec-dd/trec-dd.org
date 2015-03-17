#!/bin/env python
'''This script illustrates how to download and access the `local
politics` subcorpus within TREC DD

This particular corpus is a selection of the TREC KBA 2014
StreamCorpus that has already been tagged with Serif NER, and is
organized into hourly directories based on the origination time stamp
on each document.

The full list of files is available at
https://aws-publicdatasets.s3.amazonaws.com/trec/dd/local-politics-streamcorpus-v0_3_0-s3-paths.txt.xz
and that file must be downloaded to your local directory in order for
this script to work.

The filtering process that generated this data set used these
substrings:
https://aws-publicdatasets.s3.amazonaws.com/trec/dd/local-politics-domain-substrings-filtering.txt

and this streamcorpus_pipeline configuration file:
https://aws-publicdatasets.s3.amazonaws.com/trec/dd/local-politics-streamcorpus-pipeline-filter-config.yaml
https://aws-publicdatasets.s3.amazonaws.com/trec/dd/local-politics-streamcorpus-pipeline-filter-domains.txt.xz.gpg

and this command:
streamcorpus_pipeline -c local-politics-streamcorpus-pipeline-filter-config.yaml -i <path to input S3 file>

'''
## python standard library components
import cbor
from cStringIO import StringIO
from itertools import chain
import logging
from operator import attrgetter
import os
import sys
import traceback
import time

## these python packages require installation; consider using a
## virtualenv, which you can install on Ubuntu like this:
# sudo apt-get install python-virtualenv liblzma-dev python-dev
# virtualenv ve
# source ve/bin/activate
# pip install requests backports.lzma streamcorpus
## installation on CentOS/RHEL is similar using yum instead of apt-get
from backports import lzma
import requests
from streamcorpus import Chunk, decrypt_and_uncompress, compress_and_encrypt

logging.basicConfig()
logger = logging.getLogger()

s3_http_host = 'https://aws-publicdatasets.s3.amazonaws.com/'
s3_path_prefix = 'trec/dd/local-politics-streamcorpus-v0_3_0/'
s3_paths_fname = 'local-politics-streamcorpus-v0_3_0-s3-paths.txt.xz'
if not os.path.exists(s3_paths_fname):
    sys.exit('please download %strec/dd/%s' % (s3_http_host, s3_paths_fname))

for path in lzma.open(s3_paths_fname):
    s3_path = s3_path_prefix + path.strip()
    url = s3_http_host + s3_path
    logger.info( url )
    retries = 0
    max_retries = 10
    while retries < max_retries:
        retries += 1
        sys.stderr.flush()
        try:
            resp = requests.get(url)
            errors, data = decrypt_and_uncompress(resp.content, gpg_private='trec-kba-rsa')
            logger.info( '\n'.join(errors) )
            for si in Chunk(file_obj=StringIO(data)):

                rec = {
                    'url': si.abs_url,
                    'timestamp': si.stream_time.epoch_ticks,
                    'request': None,  ## not part of this data set
                    'response': {
                        'headers': [
                            ['Content-Type', 'text/html'],
                        ],
                        'body': si.body.clean_html,
                        ## alternatively, could use si.body.raw and
                        ## si.body.media_type for the Content-Type
                        ## header, but that would cause the Serif NER
                        ## to be useless to teams...
                    },
                    'key': None,
                    'imported': None,
                }

                print cbor.dumps(rec)

                ## do something with the data
                logger.info('%d bytes of html, or %d bytes of tag-stripped clean_visible, ' +
                       'and %d sentences with %d tokens') % (
                        len(si.body.clean_html), len(si.body.clean_visible), 
                        len(si.body.sentences['serif']),
                        len(list(chain(*map(attrgetter('tokens'), si.body.sentences['serif'])))),
                        )
            break # break out of retry loop
        except Exception, exc:
            logger.info( traceback.format_exc(exc) )
            logger.info( 'retrying %d of %d times to fetch and access: %s' % (retries, max_retries, url) )
            time.sleep(1)

