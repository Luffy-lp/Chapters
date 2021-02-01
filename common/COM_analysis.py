from common.COM_data import MyData
import inspect
import re
import sys
import types
from case.test_case import *
from common import COM_utilities
from common.COM_path import *
import importlib
from time import sleep
from common.COM_path import *
from airtest.core.api import assert_equal
from airtest.report.report import simple_report
from scenes.scenes_login.SCN_gamestart import GameStart
from scenes.scenes_login.SCN_gameloaded import GameLoaded
from scenes.scenes_login.SCN_newuser import NewUserGuide
from scenes.scenes_discover.SCN_discover import Discover
from scenes.scenes_visualbook.SCN_bookread import BookRead
from scenes.scenes_visualbook.SCN_bookdetail import BookNewDetail
from scenes.scenes_login.SCN_signin import SignIn
from scenes.SCN_pageTurn import PageTurn
from scenes.scenes_community.SCN_chapteredit import ChapterEdit
from scenes.scenes_community.SCN_community import Community
from scenes.scenes_community.SCN_readUGCbook import ReadUGCBook


# import allure


class MyAnalysis():
    function_regexp = re.compile(r"^\$\{(\w+)\(([\$\w =,]*)\)\}$")
    stepdata_list = []
    Runlist = []
    Case_info = {}
    index = 0
    Case_dir = {}
    Runlist_dir = {}
    popup_list=[]
    path = os.path.join(path_YAML_FILES, "yamlCase/casedatas.yml")
    Popuopath = os.path.join(path_YAML_FILES, "yamlCase/popup.yml")

    def __init__(self):
        self.yaml_data(self.path)
        self.getrunlist()
        self.yaml_data_popup(self.Popuopath)

    def is_functon(self, content):
        matched = self.function_regexp.match(content)
        return True if matched else False

    def parse_function(self, content):
        """解析字符串"""
        function_meta = {
            "args": [],
            "kwargs": {}
        }
        matched = self.function_regexp.match(content)
        function_meta["func_name"] = matched.group(1)

        args_str = matched.group(2).replace(" ", "")
        if args_str == "":
            return function_meta

        args_list = args_str.split(',')
        for arg in args_list:
            if '=' in arg:
                key, value = arg.split('=')
                function_meta["kwargs"][key] = value
            else:
                function_meta["args"].append(arg)

        return function_meta

    def is_function(self, tup):
        """ Takes (name, object) tuple, returns True if it is a function.
        """
        name, item = tup
        if isinstance(item, types.FunctionType):
            aa = eval(str(item.__name__))
        return

    def import_module_functions(self, modules):
        """ import modules and bind all functions within the context
        """
        for module_name in modules:
            imported = importlib.import_module(module_name)
            imported_functions_dict = dict(filter(self.is_function, vars(imported).items()))
        return imported_functions_dict

    def yaml_data(self, path):
        """解析yamlcase数据"""
        function_meta = {
            "func_name": None,
            "args": [],
            "kwargs": {}
        }
        yamldata_dir = COM_utilities.read_yaml(path)
        for i, val in yamldata_dir.items():
            dir = {}
            dir.update({"casename": val["casename"]})
            dir.update({"casedec": val["casedec"]})
            dir.update({"reportname": val["reportname"]})
            dir.update({"caseauthor": val["caseauthor"]})
            dir.update({"repeattime": int(val["repeattime"])})
            self.Case_info[i] = dir
            caselist = yamldata_dir[i]["step"]
            for k in range(0, len(caselist)):
                function_meta = self.parse_function(caselist[k])
                function_meta["func_name"] = function_meta['func_name']
                function_meta["args"] = function_meta['args']
                function_meta["kwargs"] = function_meta['kwargs']
                self.stepdata_list.append(function_meta)
            self.Case_dir[i] = self.stepdata_list
            self.stepdata_list = []
    def yaml_data_popup(self, Popuopath):
        """解析yamlcase数据"""
        function_meta = {
            "popup_name": None,
            "element": [],
            "kwargs": {}
        }
        yamldatalist = COM_utilities.read_yaml(Popuopath)
        for i in range(0, len(yamldatalist)):
            self.index = i
            caselist = yamldatalist[i][i]["step"]
            for k in range(0, len(caselist)):
                thefunction_meta = self.parse_function(caselist[k])
                function_meta["Popupname"] = thefunction_meta['func_name']
                function_meta["element"] = thefunction_meta['args']
                function_meta["kwargs"] = thefunction_meta['kwargs']
                self.popup_list.append(thefunction_meta)
            MyData.popup_dir[i] = self.popup_list
            self.popup_list = []

    def getrunlist(self):
        for k, var in self.Case_dir.items():
            for i in range(0, len(var)):
                args = var[i]["args"]
                func_name = var[i]["func_name"]
                item = {"args": args, "func_name": func_name}
                self.Runlist.append(item)
            self.Runlist_dir[k] = self.Runlist
            self.Runlist = []

# MyAnalysis1=MyAnalysis()
# MyAnalysis1.yaml_data()