import os
import MySQLdb
import sys

from subprocess import Popen, PIPE
import subprocess
from waldb_globals import *

MARK_SAMPLE_STATEMENT = """
UPDATE sample  
SET sample_finished = 1
WHERE SAMPLE_NAME = '{0}' AND SAMPLE_ID = {1}
"""

if __name__ == "__main__":

    # parse command 
    sample_name = sys.argv[1]
    sample_id = sys.argv[2]
    aa_vcf = sys.argv[3]
    bam_file = sys.argv[4]

    p1 = subprocess.call(['python', 'data_prepare_variants_local.py', sample_name, sample_id, aa_vcf])
    p2 = subprocess.call(['python', 'data_load_variants.py', sample_name, sample_id])
    p3 = subprocess.call(['python', 'data_prepare_cvg_bins_local.py', sample_name, sample_id, bam_file])
    p4 = subprocess.call(['python', 'data_load_cvg_bins.py', sample_name, sample_id])
    
    # mark it as finished. 
    database = "atavdb"
    
    db = get_local_connection(database)
    try:
        cur = db.cursor()
        statement = MARK_SAMPLE_STATEMENT.format( sample_name, sample_id)

        cur.execute(statement)
        db.commit()
    except MySQLdb.InternalError:
        print ("{statement} failed".format(statement=statement))
        # logger.error("{statement} failed".format(statement=statement))
    finally:
        if db.open:
            db.close()