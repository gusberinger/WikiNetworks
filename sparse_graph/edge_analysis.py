from database import Database
from helpers import *
import pandas as pd

db = Database(DATABASE_PATH)

links_query = """SELECT id, outgoing_links_count, incoming_links_count
FROM links
ORDER BY incoming_links_count DESC
LIMIT 1000
"""

links_df = pd.read_sql(links_query, db.sdow_conn)
print(links_df.head())



pages_df = pd.read_sql("SELECT id, title FROM pages WHERE is_redirect=0", db.sdow_conn)
print(pages_df.head(100))



df = pd.merge(links_df, pages_df, how="left", on="id")
del pages_df

print(df.head())
df.to_csv(IN_EDGE_REPORT_PATH)
