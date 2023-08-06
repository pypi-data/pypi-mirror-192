import os

from sihodictapi.mdict_query import IndexBuilder


class Crown:
    """
    超級クラウン中日辞典/クラウン日中辞典
    """
    _current_dir = os.path.dirname(os.path.abspath(__file__))
    _builder_jc = IndexBuilder(os.path.join(_current_dir, '超級クラウン日中辞典.mdx'))
    _builder_cj = IndexBuilder(os.path.join(_current_dir, '超級クラウン中日辞典.mdx'))

    @classmethod
    def dict_search(cls, text: str) -> (list, list):
        """
        查词
        :param text: 输入
        :return: (中日辞典结果列表, 日中辞典结果列表)
        """
        cj_results = cls._builder_cj.mdx_lookup(text)
        jc_results = cls._builder_jc.mdx_lookup(text)
        return cj_results, jc_results
