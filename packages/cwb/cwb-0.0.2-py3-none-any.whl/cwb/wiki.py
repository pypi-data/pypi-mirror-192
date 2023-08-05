# -*- coding: utf-8 -*-
"""Ceruleanbot
~~~~~~~~~~~~~~~~~~~~~"""

from requests import get as _get
from typing import Union
import time

if __package__ == "": # in package
    from core.query import categorymembers, recentchanges
    from core.color_cmdline import cprint, COLORS
    from core.search import search as __search
    from core.page import Page as _Page
    from core.api import session as _session
    
elif __package__ == "ceruleanwikibot": # out of package
    from .core.query import categorymembers, recentchanges
    from .core.color_cmdline import cprint, COLORS
    from .core.search import search as __search
    from .core.page import Page as _Page
    from .core.api import session as _session


class wiki:
    """
    mediawiki site class"""

    def __init__(self, url: str ="https://ko.wikipedia.org", apiprefix="/w"):
        """URL is mediawiki site"""

        try:
            _get(url + apiprefix, timeout=30)

        except ConnectionError as e:
            print(e)
            return

        self.domain = url
        self.apipath = f"{url}{apiprefix}/api.php"

        self.session = _session(self.apipath)
        """세션 객체"""

        self.page = _Page(self.session)
        """(object).page.cont 페이지 객체

        self.setpage로 페이지 제목을 설정하고
        self.page.get()으로 페이지 내용 얻기"""

        self.pagelist = Pagelist()

# -------------
# ------------- about wiki
# -------------

    def get_wiki_info(self):
        json = self.session.get({
            "action": "query",
            "meta": "siteinfo",
            "siprop": "extensions|general"
        })
        if json.__len__() == 0:
            return

        if "query" not in json or "general" not in json["query"]:
            cprint("query error", COLORS.ERROR)
            print(json)
            raise Exception

        return json["query"]


    def view_front_page(self):
        res = self.session.get_by_url(self.domain)
        if res:
            print(res.content.decode())
        else:
            print("fail")

# -------------
# ------------- user handler section
# -------------
    def print_user_info(self):
        """print user info

        Example:
            username: asdf
            edit count: 300
        """
        info = self.session.get_userinfo(['editcount'])

        print(f"""사용자 이름: {info['name']}
편집 횟수: {info['editcount']}""")

    def login(self, username: str, password: str, bot_flag: bool = False):
        """사이트 로그인 일반 사용자도 가능

        봇 계정도 가능하지만 봇을 이용하려면 봇 비밀번호 설정 권장, 형식 : username@passwd
        사이트 위키 특수문서에서 발급 가능.
        """
        self.session.login(username, password)
        self.session.bot_flag = bot_flag

        return self.session

    def logout(self):
        """로그아웃"""
        self.session.logout()

# --------- add page to page list
    def addpage(self, pagetitle: str):
        """
        add page to edit or read
        """
        self.pagelist.add(pagetitle)

        print(pagetitle)

# --------- page search methods

    def wikisearch(self, keyword):
        """검색하기"""
        return __search(self.apipath, keyword)

    def pages_in_category(self,
        category_name: str,
        namespace = '',
        pagetype = 'page',
        sortmethod = 'title',
        startsortkey: Union[str, None] = None,
        endsortkey: Union[str, None] = None,
        sortdir = "desc"
    ):

        _list = categorymembers(
            self.session, category_name, namespace,
            pagetype, sortmethod, startsortkey, endsortkey, sortdir)

        self.pagelist += _list
        return _list

    def recent_changes(self,
        days=0, minutes=0, hours=0, weeks = 0,
        timestart = "", timeend = "",
        sortdir = "older",  # "older | newer"
        namespace = "",
        user = "",
        limit = 50,
        pagetype = "page",  # page | file | subcat
        prefix = ""
    ):
        
        list = recentchanges(self.session,
        days, minutes, hours, weeks,
        timestart, timeend,
        sortdir, namespace, user, limit = limit, prefix= prefix)

        self.pagelist += list

        return list

# ----------- simply get data with url
    def get_by_url(self, url: str = "") -> dict:
        """API URL을 직접 입력해서 데이터 받기"""
        return self.session.get_by_url(url).json()

# ------------- file section
    def upload_file(
        self,
        filedir_source: str,
        filedir_dest: str,
        category: str = "",
        licence: str = "",
        text: str = "",
        date: str = "",
        author: str = "",
        etc: str = "",
        file_source: str = "",
    ):
        """파일 업로드

        source : 파일 소스

        filename : 파일 이름(확장자 포함)

        category : 분류 [[분류:예시]]

        licence : 라이선스 : 각 사이트 라이선스 틀 작성

        text : 파일 문서 텍스트 예시 :

        == 파일의 설명 ==

        {{파일 정보

        |설명 =

        |출처 =

        |날짜 =

        |만든이 =

        |기타 =

        }}

        == 라이선스 ==
        """

        if text == "":
            text = f"""
== 파일의 설명 ==
{'{{'}파일 정보
|설명 =
|출처 = {file_source}
|날짜 = {date}
|만든이 = {author}
|기타 = {etc}
{'}}'}
== 라이선스 ==
"""
        if licence != "":
            text += "{{" + licence + "}}"

        text = text + category

        data = {
            "text": text,
            "filename": filedir_dest,
            "action": "upload",
            "async": 1,
            "ignorewarnings": 1
        }

        data = self.session.post(data,
        files={"file": (filedir_dest, open(filedir_source, "rb"), "multipart/form-data")})

        if data.__len__() == 0:
            return

        if "upload" in data:
            print(data["upload"]["filename"])
        else:
            cprint(data["error"]["code"], COLORS.ERROR)

    def __del__(self):
        self.logout()

class Pagelist(list):
    """찾은 페이지 목록, 검색한 페이지들의 목록"""

    def __init__(self):
        super().__init__()

    def get(self):
        return self
        
    def __add__(self, pages: list):
        self += pages

    def __lshift__(self, page):
        self.add(page)

    def add(self, pagetitle: str):
        if type(pagetitle) == str:
            self.append(pagetitle)
        else:
            Exception("type of pagetitle is not str")
            return

    def print(self):
        for page in self:
            print(page['title'])

