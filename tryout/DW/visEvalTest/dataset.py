# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import json
from pathlib import Path
import os


class Dataset:
    def __init__(
        self,
        folder: str,
        table_type: str = "all",
        with_irrelevant_tables: bool = False,
    ):
        self.folder = folder
        dict_name = "visEval"
        if table_type in ["single", "multiple"]:
            dict_name += "_" + table_type
        dict_name += ".json"
        # for example: read visEval_single.json in viseval_dataset folder
        with open(os.path.join(folder,dict_name)) as f:
            self.dict = json.load(f)

        # read db_tables.json in viseval_dataset/.../databases folder
        # 这里面是tables name
        with open(os.path.join(folder,"databases/db_tables.json")) as f:
            self.db_tables = json.load(f)

        # dict:visEval_single.json
        def benchmark():
            # key: "8","9"
            for key in list(self.dict.keys()):
                # set "id" as same as key "8"
                self.dict[key]["id"] = key
                # set "tables" as relevant table csv path list, contain element like("/databases/db_id/table_name.csv")
                self.dict[key]["tables"] = self.__get_tables(
                    key, with_irrelevant_tables
                )
                # 类似 return 的关键字
                yield self.dict[key]

        # 是一个generator对象,每个元素都是key对应的value，value比之前增加了"id","tables"
        self.benchmark = benchmark()

    # id=key
    def __get_tables(self, id: str, with_irrelevant_tables: bool = False):
        spec = self.dict[id]
        # db_id: "activity_1"
        db_id = spec["db_id"]
        # all table name
        all_table_names = self.db_tables[db_id]
        # get relevant table name as a list
        table_names = [
            x
            for x in all_table_names
            # 从SQL语句里找到relevant table
            if x.lower() in spec["vis_query"]["VQL"].lower().split()
        ]

        if with_irrelevant_tables:
            irrelevant_tables = spec["irrelevant_tables"]
            # add irrelevant tables names to table_names
            table_names.extend(irrelevant_tables)

        # return relevant table csv path list
        tables = list(
            map(
                lambda table_name: os.path.join(f"{self.folder}/databases/", f"{db_id}/{table_name}.csv") ,
                table_names,
            )
        )

        return tables
