import os
import sys
import subprocess

from waldb_globals import *
from db_statements import *

cfg = get_cfg()
CHROMs = OrderedDict([[chromosome.upper(), int(length)]
                      for chromosome, length in cfg.items("chromosomes")])

if __name__ == "__main__":

    sample_name = sys.argv[1]
    sample_id = sys.argv[2]
    
    output_base = sample_name + ".out"
    novel_variants = output_base + ".novel_variants.txt"
    novel_indels = output_base + ".novel_indels.txt"
    novel_transcripts = output_base + ".novel_transcripts.txt"
    called_variants = output_base + ".calls.txt"
    variant_id_vcf = output_base + ".variant_id.vcf"
    matched_indels = output_base + ".matched_indels.txt"

    # database = "WalDB"
    database = "atavdb"
    min_dp_to_include = 3
    dont_load_data = False
    
    for chromosome in CHROMs.iterkeys(): 
        
        if not dont_load_data:
            db = get_local_connection(database)

            try:
                cur = db.cursor()
                for table_name, table_file, is_variant_table in (
                    ("variant_chr" + chromosome, chromosome + '.' + novel_variants, True),
                    ("indel_chr" + chromosome, chromosome + '.' + novel_indels, False),
                    ("custom_transcript_ids_chr" + chromosome, chromosome + '.' + novel_transcripts, False),
                    ("called_variant_chr" + chromosome, chromosome + '.' + called_variants, False),
                    ("matched_indels", chromosome + '.' + matched_indels, False)):
                    
                    load_statement = ( LOAD_TABLE_REPLACE if is_variant_table else LOAD_TABLE)
                    load_statement = load_statement.format( table_name=table_name, table_file=table_file )

                    cur.execute(load_statement)
                db.commit()

            finally:
                if db.open:
                    db.close()








