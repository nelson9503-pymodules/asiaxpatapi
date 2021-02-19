import requests
import html2text


class ContentExtractor:

    def __init__(self):
        pass

    def extract(self, url: str) -> dict:
        lines = self.__request_web_page(url)
        lines = self.__join_fragment_lines(lines)
        self.results = {}
        self.__check_price(lines)
        self.__check_estate(lines)
        self.__check_real_area(lines)
        self.__check_update(lines)
        self.__check_address(lines)
        self.__check_room(lines)
        self.__check_bathroom(lines)
        self.__check_floor(lines)
        self.__check_contact_person(lines)
        self.__check_contact_phone(lines)
        return self.results

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

    def __request_web_page(self, url: str) -> list:
        r = requests.get(url)
        lines = html2text.html2text(r.text).split("\n")
        return lines

    def __check_price(self, lines: list):
        for line in lines:
            if line[:3] == "HKD":
                txt = line.split(" ")[1]
                self.results["price"] = txt.replace(",", "")
                break

    def __check_estate(self, lines: list):
        for i in range(len(lines)):
            line = lines[i]
            if line == "Direct Owner":
                self.results["estate"] = lines[i+4]
                break

    def __check_real_area(self, lines: list):
        for line in lines:
            if line[:len("Saleable Area")] == "Saleable Area":
                area = ""
                for t in line:
                    if self.__is_number(t):
                        area += t
                if not area == "":
                    self.results["real area"] = area
                break

    def __check_update(self, lines: list):
        for line in lines:
            if line[:len("Updated on")] == "Updated on":
                year = ""
                month = ""
                day = ""
                txts = line.replace(",", "").split(" ")
                month_dict = {
                    "Jan": 1,
                    "Feb": 2,
                    "Mar": 3,
                    "Apr": 4,
                    "May": 5,
                    "Jun": 6,
                    "Jul": 7,
                    "Aug": 8,
                    "Sep": 9,
                    "Oct": 10,
                    "Nov": 11,
                    "Dec": 12
                }
                month = month_dict[txts[2]]
                day = txts[3]
                year = txts[4]
                self.results["post_date"] = "{:02d}-{:02d}-{:04d}".format(
                    int(day), int(month), int(year))
                break

    def __check_address(self, lines: list):
        for line in lines:
            if line[:len("Address")] == "Address":
                txt = line.split("[")[0].replace("Address: ", "")
                txt = self.__remove_abnormal_spaces(txt)
                self.results["address"] = txt
                break

    def __check_room(self, lines: list):
        for line in lines:
            if line[:len("Bedrooms")] == "Bedrooms":
                room = ""
                for t in line:
                    if self.__is_number(t):
                        room += t
                if not room == "":
                    self.results["room"] = room
                break

    def __check_bathroom(self, lines: list):
        for line in lines:
            if line[:len("Bathrooms")] == "Bathrooms":
                bathroom = ""
                for t in line:
                    if self.__is_number(t):
                        bathroom += t
                if not bathroom == "":
                    self.results["bathroom"] = bathroom
                break

    def __check_floor(self, lines: list):
        for line in lines:
            if line[:len("Floor Zone")] == "Floor Zone":
                self.results["floor"] = line.replace(
                    "Floor Zone", "").replace(" ", "").replace(":", "")
                break

    def __check_contact_person(self, lines: list):
        for i in range(len(lines)):
            line = lines[i]
            if line == "Contact Details":
                self.results["contact_person"] = lines[i+1]
                break

    def __check_contact_phone(self, lines: list):
        for i in range(len(lines)):
            line = lines[i]
            if line == "Contact Details":
                for i2 in range(i, len(lines)):
                    if "tel:" in lines[i2]:
                        tel = lines[i2].split("tel:")[1]
                        phone = ""
                        for t in tel:
                            if self.__is_number(t):
                                phone += t
                        if not phone == "":
                            self.results["contact_phone"] = phone
                        break
                break

    def __is_number(self, txt: str) -> bool:
        if txt in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return True
        return False
