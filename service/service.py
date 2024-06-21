
import re


class Service:
    @staticmethod
    def remove_links(string):
        pattern = r'<a.*<\/a>'
        result = re.sub(pattern, '', string)
        return result
