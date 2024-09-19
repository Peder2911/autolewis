
import hashlib
import os
import autolewis.ingest
import sqlite3
import pycountry
import pdb

if __name__ == "__main__":
    con = sqlite3.connect("db.sqlite")

    con.execute("""create table if not exists countries (
                id string primary key,
                name string
        )
    """)

    con.execute("""
        create table if not exists articles (
            id string primary key, 
            country string,
            content text,
            foreign key (country) references countries(id)
                on delete cascade
                on update no action
        )
    """)

    country_name = "Afghanistan"
    country_code = pycountry.countries.search_fuzzy(country_name)[0].alpha_3

    con.execute("insert or ignore into countries(id,name) values (?,?)", (country_code, country_name))
    con.commit()
    for file_id,file in enumerate(os.listdir("data")):
        articles = autolewis.ingest.extract_articles("data/"+file)
        for article_id,article in enumerate(articles):
            id_string = f"{country_code}-{file_id}-{article_id}"
            con.execute("insert or ignore into articles(country,id,content) values (?,?,?)", (country_code, id_string, article))
        con.commit()
