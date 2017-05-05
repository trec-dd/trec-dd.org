

www:
	s3cmd -c ../dot-s3cfg-trec-dd.org  del --recursive --force  s3://trec-dd.org/
	s3cmd -c ../dot-s3cfg-trec-dd.org  put --recursive --acl-public trec_dd/ s3://trec-dd.org/


clean-test:
	s3cmd -c ../dot-s3cfg-trec-dd.org-test	del --recursive --force		s3://test-trecdd2017/

test: clean-test
	s3cmd -c ../dot-s3cfg-trec-dd.org-test  put --recursive --acl-public	trec_dd/ s3://test-trecdd2017/	
