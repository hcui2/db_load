# db_load

This repo contains some simple demo scripts for processing vcf files, bam files and uploading the results to the ATAVdb. Please note: these codes are not intended to be applied into production pipeline directly, only serving as a demo. We advise the user to customize the code for your own production pipeline.  

## Requirement
* Conda package management system
* Docker setup for atavdb  
* mysql client

## Step 0: set up atavdb with docker and run it
1. Please check the documentation to set up atavdb and run it with docker. 
2. Then cd to this repo folder
```
cd db_load
```
3. Besides, set up a separate database _homo_sapiens_variation_87_37_, and import the data into the databse. _homo_sapiens_variation_87_37_ is used to calcualte the polyphen score for missense variants. 
```
wget https://www.dropbox.com/s/gdduk6yt58teilx/homo_sapiens_variation_87_37.sql
mysql -h 127.0.0.1 -uroot -proot -P 3333 -e "create database homo_sapiens_variation_87_37" 
mysql -h 127.0.0.1 -uroot -proot -P 3333 homo_sapiens_variation_87_37 < homo_sapiens_variation_87_37.sql
```


## Step 1: download the test sample input data with the following commands
```
wget https://www.dropbox.com/s/qyzv4jngjbqflet/NA12878_2.2.realn.recal.bai
wget https://www.dropbox.com/s/39mqnn4ibtkvf4n/NA12878_2.2.realn.recal.bam
wget https://www.dropbox.com/s/40rqppbjblprfxa/NA12878_2.2.analysisReady.annotated.vcf.gz.tbi
wget https://www.dropbox.com/s/os5bcxbo1gu5q8e/NA12878_2.2.analysisReady.annotated.vcf.gz
```

## Step 2: download some dependency files 
These files are used during parsing the sample vcf and bam files. 
1. Download block id file:
```
wget https://www.dropbox.com/s/1lw447bsikimein/Roche_SeqCap_EZ_Exome_v3_capture_1kbBlocksIds.txt
```
2. Download human genome reference file:
```
wget https://www.dropbox.com/s/l09is4mmq2vw62y/hs37d5.fa.gz
gunzip hs37d5.fa.gz
```

## Step 3: compile DP1KbBins_rc1.cpp
This cpp program is used to generate the bin data from sample bam files. 
```
g++ -o DP1KbBins_rc1 DP1KbBins_rc1.cpp -lm
```

## Step 4: set up a conda virtual environment 
```
conda env create -f environment.yml
source activate dbload
```

## Step 5: initialize sample in atavdb 
1. prepare a csv file containing relevent sample information similar to the demo_sample.csv

2. run the script below to initialize them in atavdb
```
python init_samples.py demo_sample.csv 
```

## Step 6: parsing sample vcf file and bam file and uploading them to the atavdb 

* run the script below to parse and upload sample to atavdb. This completes the uploading sample and variant data to atavdb. 
```
python import_sample.py NA12878_2 2 NA12878_2.2.analysisReady.annotated.vcf.gz NA12878_2.2.realn.recal.bam
```
Here NA12878_2 is a user defined sample name; 2 is sample id.  

* OR you can parse the bam file and vcf file separately with the commands below. 
    * parse the bam file and upload converage bin data: 
    ```
    python data_prepare_cvg_bins_local.py NA12878_2 2 NA12878_2.2.realn.recal.bam
    python data_load_cvg_bins.py NA12878_2 2
    ```

    * parse the vcf file and upload the variant data:
    ```
    python data_prepare_variants_local.py NA12878_2 2 NA12878_2.2.analysisReady.annotated.vcf.gz
    python data_load_load_variants.py NA12878_2 2
    ```

