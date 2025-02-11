import os
import MySQLdb
import sys

from waldb_globals import *

INSERT_SAMPLE_STATEMENT = """
LOAD DATA LOCAL INFILE '{data_file}' INTO TABLE sample  
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(@sample_id, @sample_name, @sample_type, @capture_kit)
SET sample_id=@sample_id, sample_name=@sample_name, sample_type=@sample_type, capture_kit=@capture_kit, 
available_control_use = 1;
"""

if __name__ == "__main__":

    # parse command 
    sample_csv_file = sys.argv[1]
    # database = "WalDB"
    database = "atavdb"
    
    db = get_local_connection(database)
    try:
        cur = db.cursor()
        statement = INSERT_SAMPLE_STATEMENT.format(
            data_file=sample_csv_file)

        cur.execute(statement)
        db.commit()
    except MySQLdb.InternalError:
        print ("{statement} failed".format(statement=statement))
        # logger.error("{statement} failed".format(statement=statement))
    finally:
        if db.open:
            db.close()



