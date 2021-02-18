import requests
import html2text


class CoverExtractor:

    def __init__(self):
        pass

    def extract(self, page: int) -> dict:
        url = "https://hongkong.asiaxpat.com/property/direct-owner-apartments-for-rent/{}/".format(
            page)
        lines = self.__request_web_page(url)
        lines = self.__join_fragment_lines(lines)
        results = {}
        for i in range(len(lines)):
            if lines[i] == "Direct Owner":
                result = self.__check_property(lines, i)
                if len(result) > 0:
                    results[result["title"]] = result
        return results

    def __join_fragment_lines(self, lines: list) -> list:
        newlines = []
        cache = ""
        for line in lines:
            line = self.__remove_abnormal_spaces(line)
            if line == "" and not cache == "":
                newlines.append(cache)
                cache = ""
            elif not line == "":
                cache += line
        if not cache == "":
            newlines.append(line)
        return newlines

    def __remove_abnormal_spaces(self, txt: str) -> str:
        while len(txt) > 0 and txt[0] == " ":
            txt = txt[1:]
        while len(txt) > 0 and txt[-1] == " ":
            txt = txt[:-1]
        while "  " in txt:
            txt = txt.replace("  ", " ")
        return txt

    def __check_property(self, lines: list, i: int) -> dict:
        results = {}
        for i2 in range(i+1, i+25):
            if lines[i2] == "Direct Owner":
                break
            if lines[i2][0] == "[" and "/property/direct-owner-apartments-for-" in lines[i2] and not "title" in results:
                results["title"] = self.__extract_between(
                    lines[i2], "[", "]")[0]
                txts = self.__extract_between(lines[i2], "(", ")")
                for txt in txts:
                    if "/property/direct-owner-apartments-for-" in txt:
                        url = txt
                        break
                url = url.split(" ")[0]
                results["url"] = "https://hongkong.asiaxpat.com" + url
            if lines[i2][:4] == "* [!":
                url = lines[i2]
                if not "photos" in results:
                    results["photos"] = []
                results["photos"].append(
                    "https://hongkong.asiaxpat.com"+self.__extract_between(url, "(", ")")[0])
        return results

    def __extract_between(self, txt: str, left: str, right: str):
        result = []
        record = False
        cache = ""
        for t in txt:
            if t == left:
                cache = ""
                record = True
            elif t == right:
                if not cache == "":
                    result.append(cache)
                record = False
            elif record == True:
                cache += t
        return result

    def __request_web_page(self, url: str) -> list:
        r = requests.get(url)
        lines = html2text.html2text(r.text).split("\n")
        return lines
