**************************************************************************
** This is the readme file of  the user simulator (jig) package for the TREC 2015 Dynamic Domain (DD) Track.
** The package is for research use only. 

** For technical questions, please submit your request to google group https://groups.google.com/forum/#!forum/trec-dd 
 
**************************************************************************

** What is inside this package: 

a user simulator (jig), 
a sample search system (built on top of Lemur) interacting with the jig, 
a scorer outputs the cubetest scores, 

**************************************************************************

** Installation: 
  
   1. Unpack trec_dd.tar.gz 
        > gunzip trec_dd.tar.gz
        > tar -xvf trec_dd.tar

   2.  Install dossier.label package
	> pip install dossier.label
	
	Our python code works the best under python 2.7. You will also need to install python virtualenv before install the dossier.label package. 

   3. install lemur/Indri  (for the sample DD system)
   * Download the Lemur/Indri software package indri-5.0.tar.gz from https://sourceforge.net/projects/lemur/files/lemur/indri-5.0/. Or, you can use the one provided in our package. 
   * Unpack the Lemur/Indri software package
   * Assume you put Lemur/Indri into a directory named /yourhomedirectory/indri-5.0/, install it by the following commands. Note you will need to enable the --with-lemur option.
	> cd indri-5.0
	> mkdir install
	> chmod +x ./configure
        > ./configure --prefix=/yourhomedirectory/indri-5.0/install/ --with-lemur=/yourhomedirectory/indri-5.0/install/
        > make
        > make install

   4.   move the unpacked directory under the lemur directory, that is,  
mv trec_dd_2015_release /yourhomedirectory/indri-5.0/. 

   5. cd  /yourhomedirectory/indri-5.0/trec_dd_2015_release 

   6. sh install.sh

You will see a bin directory in /yourhomedirectory/indri-5.0/trec_dd_2015_release. 

Your topics (with ground truth) can be downloaded from the TREC Active Participants Home Page. Copy it and put it under ./trec_dd_2015_release/truth_data/topics.xml

Congratulations for a successful installation!!

**************************************************************************

** How your system interacts with the simulator (jig): 

Your systems should call python jig/jig.py to get feedback for each iteration of retrieval. The program outputs a json dumped string. It provides feedback to your returned documents. Only positive feedback will be shown be shown.  Use the following command:

            > python jig/jig.py -c config_file step topic_id docno1 docno2 docno3 docno4 docno5
            
            - config_file: the path to the configuration file. There is an example config file located at ./trec_dd_2015_release/jig/config.yaml. It points to the path of the topics.xml file. 
            - topic_id: the id of the topic you are working on
            - docno1, docno2 ...: the five document ids that your system returned. It needs to be the document ids in TREC DD datasets.    
		        
Each feedback is a tuple of (docid, subtopic_id, passage_text, rating) for a document: 

- docid: the id of a returned document
- subtopic_id: the id of a relevant subtopic that your returned document covers 
- passage_text: the content of a relevant passage that your returned document covers 
- rating: the relevance grade provided by NIST assessors. 1: marginally relevant, 2: relevant, 3: highly relevant, 4: key results. The relevance grades refer to the relevance level of your document to the whole topic. 

Note that subtopic_ids are global ids, i.e., a certain topic might contains subtopic with id 12, 45, 101, 103...
                

**************************************************************************

** Test your installation with a sample DD system. 

The current sample system is built on top of indri. Assume you have built an indri index for TREC DD corpus (here is where to get the corpus, http://trec-dd.org/dataset.html). To build an indri index, you will need to use /yourhomedirectory/indri-5.0/install/bin/IndriBuildIndex  (please see how to build an indri index at http://www.lemurproject.org/lemur/indexing.php#IndriBuildIndex) 
Note that you will need to come out with your own system, however feel free to start from this very simple system. This sample system stops after retrieving 200 documents. Your own system should be smarter than this stopping criterion. 

Then, run the following command: 

sh run_lemur_dd.sh 

NOTE: run_lemur_dd.sh executes a program  'lemur_dd':

	Usage:./bin/lemur_dd -topics=<topic file> -domain=<current domain> -runid=<run tag> -index=<repository> -config=<configuration file> [-topicNum=<topic id> -count=<result number> -rule=<smoothing rules>]
	Detail:
		topic file: the topics.xml file
		current domain: one string from the following list Illicit_Goods/Ebola/Local_Politics/Polar
		run tag: name for a run
		repository:  indri index built for a domain
		configuration file: the configuration file used to call jig
		topic id: topic id
		result number: number of retrieval results for a topic, default is 200
		smoothing rules:  Lemur retrieval parameters
		
	For example, for topic 55  "Theresa Spence" :

>$./bin/lemur_dd -topicNum=51 -topics=truth_data/topics.xml -config=jig/config.yaml -rule=method:d,mu:5000 -domain=Ebola -index=/data1/trecdd/index/ebola_html_01_03_tweets -runid=GU_RUN1

       Example feedback for topic 55 "Theresa Spence" :
       
topic 55 query:Theresa Spence
feedback:[[], [], [["1323453660-374c2bc4b4371a227d4b9ff703c9750e", "32", "My community will not consider third-party managers nor pay for them out of our already depressed band support funding budget,\u00e2\u0080\u009d Attawapiskat First Nation Chief Theresa Spence wrote, mostly in capital letters, in a response to Aboriginal Affairs Minister John Duncan on Friday.\n\n ", "4"]], [], []]

feedback:[[], [], [], [], []]

feedback:[[], [], [], [["1323124200-1f699d3ee9a338089fa0bc6ec612b173", "32", "The government said earlier it had chosen Jacques Marion, from the accounting and consulting firm BDO Canada, as its third-party manager for Attawapiskat. Marion was to exercise signing authority for all department spending and would decide which band staff are required to run its program and services.\n\n \nSpence said the minister responsible for First Nations &quot;didn&apos;t listen.&quot;\n\n \n&quot;We&apos;d like to work together but put third party away \u00c3\u00a2\u00c2\u0080\u00c2\u00a6 We&apos;ve demonstrated we have our deficit down. We don&apos;t need a banker to come and tell us what to do,&quot; the chief told Solomon.\n\n ", "4"]], []]

feedback:[[["1322812020-35e06badddb1bd58ca16a34dfffedef3", "70", "Roughly $11 million in debt, the Attawapiskat council has been on financial alert since at least July 2010, when federal officials required it to engage a professional co-manager to monitor spending and accounting procedures.\n\n  \nThe council hired Clayton Kennedy, who admits he is in a romantic relationship with Spence.\n\n  \n\u00e2\u0080\u009cYes, I am,\u00e2\u0080\u009d he said Thursday. \u00e2\u0080\u009cThere is a conflict-of-interest policy in place.\u00e2\u0080\u009d\n\n  \nKennedy said he does not make recommendations to the chief or her deputy but to the council as a whole, and so his personal relationship with Spence should not be a factor.\n\n  \n\u00e2\u0080\u009c", "4"]], [], [], [], []]

feedback:[[], [], [], [], []]

**************************************************************************

** Run Format

We use the TREC submission format as the following: 

          topic_id Q0 doc_no doc_rank ranking_score run_id iteration_id


   For instance:
   
51	Q0	ebola-51c6d350e897850b1b1b654e54fba32e8f20c75642d3a957c8ff138508085221	1	-6.07989	GU_RUN1	1
51	Q0	ebola-0bbd59454ca76fec0751feb64f22a3513babc4c059219984adca8dd15b12a800	2	-6.08048	GU_RUN1	1
51	Q0	ebola-58c00f82c27c9497992dc3f2be5d21fda5cb7f3980de8d7d469454e97113c394	3	-6.22642	GU_RUN1	1
51	Q0	ebola-f31b1ece713598930721e946c35ae0cc5c1be44c6c6740989699c531df764009	4	-6.23271	GU_RUN1	1
51	Q0	ebola-9bcab76e9411db650b6831c177218820c4c181d4d2da4722db5b57b7e9f43f0c	5	-6.23287	GU_RUN1	1
51	Q0	ebola-5682a84bc342c37a7906be01d77a5c68ed2a60395ad6a39460f7228307a8202f	1	-6.27632	GU_RUN1	2
51	Q0	ebola-7c5e0162a9af78dbea4eb0ff7be8f9b7a12b5628d6745282f8c93945360696ca	2	-6.32298	GU_RUN1	2
51	Q0	ebola-0ffc5b206d49788a68b024408f5a8f9775a2f151582b10950dd37284a00ae510	3	-6.33974	GU_RUN1	2
51	Q0	ebola-cf16ae103c906fc433919d92cc4cea1535e4c8aae7eb9e36c7b36f35e2e90565	4	-6.35099	GU_RUN1	2
51	Q0	ebola-6836b94bfe72c21436df2cbc5e7543ed1e12a021a2872c4754949418704109d3	5	-6.38137	GU_RUN1	2
51	Q0	ebola-69501fadea9c865300e141746188af120ded70ab7e5591611c1c5546b5b767c3	1	-6.38475	GU_RUN1	3
51	Q0	ebola-f42cb7bdafa9219f1891ed269746fbfba67e574e091b47249aab2b8f5f7c6748	2	-6.38526	GU_RUN1	3
51	Q0	ebola-103918db07a6d95104a015c4c50042acc9384ff5a5a0c80ef11d98fbf846f5ff	3	-6.3859	GU_RUN1	3
51	Q0	ebola-6c94104def405355267ae3c033495f0e5ef306e3cb8a79726f6a623c6cf588e9	4	-6.38658	GU_RUN1	3
51	Q0	ebola-4a83026d3eabe1576fa7004971b15ac5d2d5aca356a65a7333094da8f9804327	5	-6.38679	GU_RUN1	3

    NOTE that the last column is new, which shows the count of the search iterations for that line of results.      	           
	           
**************************************************************************
 
** The scorer used in TREC DD is cube test. score a submitted run using cubetest.pl

   Usage: perl ./scorer/cubeTest.pl qrel_file run_file cut_off
   
   - qrel: qrel file. It is a trec qrel file that converted from topics.xml. Its format is topic_id subtopic_id doc_no rating. 

   - run_file: Your run for submission.  It is in TREC format. 

  - cutoff: the number of iterations where you run cubetest over your results

   for example: perl scorer/cubeTest.pl truth_data/qrel.txt output/GU_RUN1 10 
	    
**************************************************************************

** description about utils:
	* getDocLength doc_id index_path : return the document length
	* getDocContent doc_id index_path : return the document content
	* getParseDoc doc_id index_path : return the parsed document content
	* krovetz_stem text : stem text using the krovetz stemmer
	* cosine_similarity text1 text2 : calculate the cosine similarity score between two pieces of text. (it is better to use stemmed text as inputs to this function)




