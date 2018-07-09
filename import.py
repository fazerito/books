import pandas as pd

df = pd.read_csv('books.csv')
df.columns = [c.lower() for c in df.columns]

from sqlalchemy import create_engine

engine = create_engine("postgres://dkhxrkcvbzxsjq:4c557995c15fa7c3e4f576cf7e743d64514099c3ddba7663d729c2a392e15925@ec2-54-247-79-32.eu-west-1.compute.amazonaws.com:5432/d1ason4t4rs4tf")
df.to_sql("books", engine, if_exists="replace")
