**************************************************************************
** This is the readme file of  the user simulator (jig) package for the TREC 2015 Dynamic Domain (DD) Track.
** The package is for research use only. 

** For technical questions, please submit your request to google group https://groups.google.com/forum/#!forum/trec-dd 
 
**************************************************************************

** What is inside this package: 

a user simulator (jig), 
a sample search system (built on top of Lemur) interacting with the jig, 
a scorer outputs the cubetest scores, 

NOTE: We support both exact match and similarity match of returned documents to ground truth. To enable your system interact with the jig with similarity matches, you will need to install the Lemur/Indri package from the lemurproject.org.  Otherwise, only exact match will be enabled for your system. 

**************************************************************************

** Installation: 


1. install lemur/Indri 
   * Download the Lemur/Indri software package indri-5.0.tar.gz from https://sourceforge.net/projects/lemur/files/lemur/indri-5.0/. Or, you can use the one provided in our package. 
   * Unpack the Lemur/Indri software package
   * Assume you put Lemur/Indri into a directory named /yourhomedirectory/indri-5.0/, install it by the following commands. Note you will need to enable the --with-lemur option.
	> cd indri-5.0
	> mkdir install
	> chmod +x ./configure
        > ./configure --prefix=/yourhomedirectory/indri-5.0/install/ --with-lemur=/yourhomedirectory/indri-5.0/install/
        > make
        > make install
        
2. Unpack trec_dd.tar.gz 
gunzip trec_dd.tar.gz
tar -xvf trec_dd.tar

3. move the unpacked directory under the lemur directory, that is,  
mv trec_dd_2015_release /yourhomedirectory/indri-5.0/. 

4. cd  /yourhomedirectory/indri-5.0/trec_dd_2015_release 

5. sh install.sh

You will see a bin directory in /yourhomedirectory/indri-5.0/trec_dd_2015_release. 

Your topics (with ground truth) can be downloaded from the TREC Active Participants Home Page. You can put it at /yourhomedirectory/indri-5.0/trec_dd_2015_release/truth_data/truth_data.xml

Congratulations for a successful installation!!  


**************************************************************************

** How your system interacts with the simulator (jig): 

Your systems should call ./jig/jig.py to get feedback for each iteration of retrieval. 
    
 We provide two feedback modes, one is c++ with both exact and similarity match, another is python without similarity match. You could select either one to get the feedback.

    1.  To run under mode1, use the following command:

         To use only exact match: 
              python jig/jig.py -o mode1  -r runid topic_id docno1 docno2 docno3 docno4 docno5
          
         To enable similarity match (your will need to provide your path to lemur index repository, assuming you build your system on top of lemur):      
              python jig/jig.py -o mode1 -i index_path -r runid topic_id docno1 docno2 docno3 docno4 docno5
		        
NOTE: The above command line outputs a json dumped string. It provides feedback to your returned documents. Only positive feedback will be shown be shown. 

Each feedback is a tuple of (subtopic_id, passage_id, rating, confidence) for a document: 

- subtopic_id: the id of a relevant subtopic that your returned document covers 
- passage_id: the id of a relevant passage that your returned document covers 
- rating: the relevance grade provided by NIST assessors. 1: marginally relevant, 2: relevant, 3: highly relevant, 4: key results. The relevance grades refer to the relevance level of your document to the whole topic. 
- confidence: the similarity matching score from your document to a passage in the ground truth. If there is an exact of your the document you returned to a ground truth passage, the confidence is 1. 

Note that subtopic_id and passage_id are global ids, i.e., a certain topic might contains subtopic with id 12, 45, 101, 103...
                

    2. To run under mode2,  use the following command:

            python jig/jig.py -o mode2 -r runid -c config_file  [more parameters, please refer to https://github.com/trec-dd/trec-dd-simulation-harness or run 'python jig/jig.py -h' for help) 


**************************************************************************

** Test your installation with a sample DD system. 

The current sample system is built on top of indri. Assume you have built an indri index for TREC DD corpus (here is where to get the corpus, http://trec-dd.org/dataset.html). To build an indri index, you will need to use /yourhomedirectory/indri-5.0/install/bin/IndriBuildIndex  (please see how to build an indri index at http://www.lemurproject.org/lemur/indexing.php#IndriBuildIndex) 
Note that you will need to come out with your own system, however feel free to start from this very simple system. This sample system stops after retrieving 200 documents. Your own system should be smarter than this stopping criterion. 

Then, run the following command: 

sh run_lemur_dd.sh 

NOTE: run_lemur_dd.sh executes a program  'lemur_dd':

	Usage:./bin/lemur_dd -topics=<topic file> -domain=<current domain> -runid=<run tag> -index=<repository> [-topicNum=<topic id> -count=<result number> -rule=<smoothing rules>]
	Detail:
		topic file: the topics.xml file
		current domain: one string from the following list Illicit_Goods/Ebola/Local_Politics/Polar
		run tag: name for a run
		repository:  indri index built for a domain
		topic id: topic id
		result number: number of retrieval results for a topic, default is 200
		smoothing rules:  Lemur retrieval parameters
		
	For example, for topic 51  "contamination health worker" :

>$./bin/lemur_dd -topicNum=51 -topics=truth_data/truth_data.xml -rule=method:d,mu:5000 -domain=Ebola -index=/data1/trecdd/index/ebola_html_01_03_tweets -runid=GU_RUN1

       Example feedback for topic 51 "contamination health worker" :
       
topic 51 query:contamination health worker 
feedback:[[["28", "7151", "2", "0.433269"]], [["28", "7151", "2", "0.433767"]], [["28", "7151", "2", "0.445547"]], [["28", "7151", "2", "0.447769"]], [["28", "7151", "2", "0.447784"]]]

feedback:[[], [["23", "42", "4", "0.430611"], ["23", "52", "3", "0.429705"], ["28", "7151", "2", "0.439869"], ["31", "54", "3", "0.430105"], ["31", "484", "2", "0.435456"]], [["23", "37", "3", "1"], ["23", "41", "3", "1"], ["23", "42", "4", "1"], ["23", "45", "3", "1"], ["23", "52", "3", "1"], ["23", "55", "3", "1"], ["23", "62", "4", "1"], ["23", "65", "3", "1"], ["24", "38", "3", "1"], ["26", "40", "3", "1"], ["28", "44", "3", "1"], ["28", "7151", "2", "0.442506"], ["31", "54", "3", "1"], ["31", "484", "2", "0.426873"]], [["28", "7151", "2", "0.445271"]], [["28", "7151", "2", "0.441989"]]]

feedback:[[], [], [], [], []]

feedback:[[["31", "484", "2", "0.440418"]], [["31", "54", "3", "0.430053"]], [["31", "54", "3", "0.430661"]], [["31", "54", "3", "0.432469"]], [["31", "54", "3", "0.43198"]]]

feedback:[[["31", "484", "2", "0.423141"]], [["28", "7151", "2", "0.442778"]], [["28", "7151", "2", "0.442065"]], [["28", "7151", "2", "0.461145"], ["130", "7160", "2", "0.421051"]], [["28", "7151", "2", "0.460194"], ["130", "7160", "2", "0.421116"]]]

feedback:[[], [], [], [], []]

feedback:[[["31", "54", "3", "0.420531"]], [], [["23", "42", "4", "0.42016"], ["28", "7151", "2", "0.503487"], ["31", "54", "3", "0.420527"], ["122", "7248", "2", "0.424148"], ["130", "7160", "2", "0.462615"]], [], []]

feedback:[[], [], [], [], []]

feedback:[[], [], [], [], []]

feedback:[[], [["31", "54", "3", "0.42048"]], [["31", "54", "3", "0.420466"]], [], []]

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
51	Q0	ebola-5682a84bc342c37a7906be01d77a5c68ed2a60395ad6a39460f7228307a8202f	6	-6.27632	GU_RUN1	2
51	Q0	ebola-7c5e0162a9af78dbea4eb0ff7be8f9b7a12b5628d6745282f8c93945360696ca	7	-6.32298	GU_RUN1	2
51	Q0	ebola-0ffc5b206d49788a68b024408f5a8f9775a2f151582b10950dd37284a00ae510	8	-6.33974	GU_RUN1	2
51	Q0	ebola-cf16ae103c906fc433919d92cc4cea1535e4c8aae7eb9e36c7b36f35e2e90565	9	-6.35099	GU_RUN1	2
51	Q0	ebola-6836b94bfe72c21436df2cbc5e7543ed1e12a021a2872c4754949418704109d3	10	-6.38137	GU_RUN1	2
51	Q0	ebola-69501fadea9c865300e141746188af120ded70ab7e5591611c1c5546b5b767c3	11	-6.38475	GU_RUN1	3
51	Q0	ebola-f42cb7bdafa9219f1891ed269746fbfba67e574e091b47249aab2b8f5f7c6748	12	-6.38526	GU_RUN1	3
51	Q0	ebola-103918db07a6d95104a015c4c50042acc9384ff5a5a0c80ef11d98fbf846f5ff	13	-6.3859	GU_RUN1	3
51	Q0	ebola-6c94104def405355267ae3c033495f0e5ef306e3cb8a79726f6a623c6cf588e9	14	-6.38658	GU_RUN1	3
51	Q0	ebola-4a83026d3eabe1576fa7004971b15ac5d2d5aca356a65a7333094da8f9804327	15	-6.38679	GU_RUN1	3

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




