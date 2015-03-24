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
import argparse
from cStringIO import StringIO
from hashlib import md5
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
import cbor
import requests
from streamcorpus import Chunk, decrypt_and_uncompress, compress_and_encrypt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class trec_xml_file_roller(object):
    '''provides a context manager for rolling files

    '''

    def __init__(self, output_dir, max_chunk_size=500, compress=False):
        self.output_dir = output_dir
        self.max_chunk_size = max_chunk_size
        self.compress = compress

    def __enter__(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.current_file_path = None
        self.current_file = None
        self.tmp_file_path = os.path.join(self.output_dir, 'tmp.xml')
        self.total_written = 0
        return self

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        self.roll()

    def roll(self):
        '''close `current_file` and rename it to `current_file_path`

        '''
        if self.current_file is not None:
            self.current_file.close()
            ## atomic rename to final location
            os.rename(self.tmp_file_path, self.current_file_path)
            self.current_file = None

    def add(self, item):
        '''add `item` to `current_file`, opening it as temporary file if not
        already open.  This also constructs the `current_file_path`
        when it opens the temporary file.

        '''
        if self.current_file is None:
            ## construct a final path to which this fil will be moved
            ## when it rolls
            self.current_file_path = os.path.join(
                self.output_dir, 
                'trec-dd-local-politics-%d.xml' % self.total_written)
            if self.compress:
                self.current_file = gzip.open(self.tmp_file_path, 'wb')
                self.current_file_path += '.gz'
            else:
                self.current_file =      open(self.tmp_file_path, 'wb')

        ## write the data
        self.current_file.write('<DOC>\n')
        self.current_file.write('<DOCNO>%s</DOCNO>\n' % item['key'])
        self.current_file.write('<TIMESTAMP>%s</TIMESTAMP>\n' % item['timestamp'])
        self.current_file.write('<URL>%s</URL>\n' % item['url'])
        self.current_file.write('<TEXT>\n%s\n</TEXT>\n' % item['response']['body'])
        self.current_file.write('</DOC>\n')

        ## roll the files each time we reach max_chunk_size
        self.total_written += 1
        if self.total_written % self.max_chunk_size == 0:
            self.roll()



def cca_items(args):
    '''This generator takes an s3_paths_fname file, fetches the data,
    constructs a CCA record, and yields it.

    '''
    for path in lzma.open(args.s3_paths_fname):
        if args.date_hour is not None:
            if not path.startswith(args.date_hour):
                continue                
        s3_path = args.s3_path_prefix + path.strip()
        url = args.s3_http_host + s3_path
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

                    item = {
                        'key': si.stream_id,
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
                        'imported': None,
                    }
                    yield item

                    #print cbor.dumps(rec)

                    ## do something with the data
                    logger.info(
                        '%d bytes of html, or %d bytes of tag-stripped clean_visible, and %d sentences with %d tokens' % (
                        len(si.body.clean_html), len(si.body.clean_visible), 
                        len(si.body.sentences['serif']),
                        len(list(chain(*map(attrgetter('tokens'), si.body.sentences['serif'])))),
                        ))
                break # break out of retry loop
            except Exception, exc:
                logger.critical( traceback.format_exc(exc) )
                logger.critical( 'retrying %d of %d times to fetch and access: %s' % (retries, max_retries, url) )
                time.sleep(1)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--date-hour', help='If specified, then `date-hour` is *added* to `output-dir`'
                        ' and this process will filter through the lines in `s3-paths-fname` to select only'
                        ' those files that start with this date-hour. There are 11,129 date hours that you can'
                        ' find by `xzcat local-politics-streamcorpus-v0_3_0-s3-paths.txt.xz | cut -d/ -f 1 | uniq | sort -u > date-hours.txt`')
    parser.add_argument('--output-dir', help='directory for writing output files in trec/xml format')
    parser.add_argument('--max-chunk-size', default=500, type=int, help='size at which to roll chunk files')
    parser.add_argument('--compress', default=False, action='store_true', help='compress output files with gzip')
    parser.add_argument('--s3-paths-fname', default='local-politics-streamcorpus-v0_3_0-s3-paths.txt.xz')
    parser.add_argument('--s3-http-host', default='https://aws-publicdatasets.s3.amazonaws.com/')
    parser.add_argument('--s3-path-prefix', default='trec/dd/local-politics-streamcorpus-v0_3_0/')
    args = parser.parse_args()

    if not os.path.exists(args.s3_paths_fname):
        sys.exit('please download %strec/dd/%s' % (s3_http_host, s3_paths_fname))

    if args.date_hour:
        args.output_dir += '/' + args.date_hour

    with trec_xml_file_roller(args.output_dir, max_chunk_size=args.max_chunk_size, compress=args.compress) as roller:
        for item in cca_items(args):
            roller.add(item)
            logger.critical('added %r %r %s' % (item['key'], item['url'], md5(item['response']['body']).hexdigest()))


if __name__ == '__main__':
    main()
