import os
import sqlite3

from typing import Union, Callable

from core.config import Environment


class VideoMetadataLoader: 
    env = Environment()

    def __init__(self, 
                 db_name:str="metadata.db", 
                 table_name:str="video_metadata",
                 row_factory:Union[bool, Union[Callable, None]]=None): 
        try: 
            data_dir = os.path.join(self.env.root, 
                                    self.env.db_root, 
                                    db_name)
            self.con = sqlite3.connect(data_dir)
            self.con.row_factory = row_factory

            self.table_name = table_name
        except sqlite3.ProgrammingError as sql3e: 
            raise sql3e
        
    def create_table(self): 
        self.con.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL, publish_date TEXT NOT NULL, thumbnail_url TEXT NOT NULL, watch_url TEXT NOT NULL, channel_id TEXT NOT NULL, channel_url TEXT NOT NULL, author TEXT NOT NULL, keywords TEXT NOT NULL, length INTEGER NOT NULL, channel_title TEXT);")


    def create_variable(self): 
        ...

    def read_variable(self, attr:dict): 
        try: 
            target = attr.values()
            result = self.con.execute("fSELECT * FROM {self.table_name} WHERE title = ?", (target, )).fetchmany()[0]
            return result
        except: 
            raise sqlite3.OperationalError()
        
    def update_variable(self, attr:dict): 
        ...

    def delete_variable(self, attr:dict): 
        ...