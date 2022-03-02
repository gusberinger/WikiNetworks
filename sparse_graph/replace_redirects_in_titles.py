from helpers import *
import pandas as pd
from database import Database
import time


db = Database(DATABASE_PATH)


t0 = time.time()
print(f"{time.time() - t0:.2f} - Loading redirects data.")
redirects_df = pd.read_sql("SELECT * FROM redirects", db.sdow_conn)

print(f"{time.time() - t0:.2f} - Loading titles that redirect.")
titles_redirects_df = pd.read_sql("SELECT id, title FROM pages WHERE is_redirect=1", db.sdow_conn)

print(f"{time.time() - t0:.2f} - Loading titles that do not redirect.")
titles_main_df = pd.read_sql("SELECT id, title FROM pages WHERE is_redirect=0", db.sdow_conn)

print(f"{time.time() - t0:.2f} - Converting redirects data to dictionary.")
redirects_dict = pd.Series(redirects_df.target_id.values,index=redirects_df.source_id).to_dict()
del redirects_df

print(f"{time.time() - t0:.2f} - Replacing redirected page ids.")
titles_redirects_df['id'] = titles_redirects_df['id'].apply(redirects_dict.get)
new_pages_df = pd.concat([titles_main_df, titles_redirects_df])

print(f"{time.time() - t0:.2f} - Sorting dataframe.")
new_pages_df = new_pages_df.sort_values(by=['id'])
new_pages_df['title'] = new_pages_df['title'].apply(str.lower)

print(f"{time.time() - t0:.2f} - Saving dataframe.")
new_pages_df.to_csv(DUMP_PATH.joinpath("pages_data.csv"), compression="gzip", index=False)

print(f"{time.time() - t0:.2f} - Done.")


