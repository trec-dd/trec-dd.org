

www:
	s3cmd -c ../dot-s3cfg-trec-dd.org  del --recursive --force  s3://trec-dd.org/
	s3cmd -c ../dot-s3cfg-trec-dd.org  put --recursive --acl-public trec_dd/ s3://trec-dd.org/
