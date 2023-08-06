from typing import Callable, Dict, TypeVar, Generic, NamedTuple, List, Optional, Any


T = TypeVar("T")


class _WithSubCategoriser(Generic[T]):
    def __init__(self):
        self._sub: Dict[str, SubCategoriser[T]] = dict()

    def add(self, name: str, matcher: Callable[[T], bool]) -> "SubCategoriser[T]":
        if name in self._sub:
            raise Exception(f"Sub-category '{name}' is already present")
        else:
            sub = SubCategoriser(name, matcher)
            self._sub[name] = sub
            return sub

    def _sub_categorise_list(self, parent_path: str, path: str, dict_items: Dict[int, T]):
        list_matches = []
        matched = set()

        for i, sub in enumerate(self._sub.values()):
            lm = sub.categorise_list(path, f"{path}.{i}", dict_items)
            if lm is not None:
                list_matches.append(lm)
                matched.update(lm.matched_items.keys())

        not_matched = set(dict_items.keys()).difference(matched)

        return list_matches, [dict_items[n] for n in not_matched]


class ListMatch(NamedTuple):
    # The name of the sub categoriser this match comes from
    category_name: str
    # path of the parent, if any
    parent_path: Optional[str]
    # Path of this match
    path: str
    # Items matched by the categoriser
    matched_items: Dict[int, Any]
    # Matches from the children of the sub categoriser
    sub_matches: List["ListMatch"]
    # Items not matched by any children
    non_sub_matches: List[Any]

    def summarise(self, sum_func: Callable[[List], Any] = len):
        rec = {
            "category_name": self.category_name,
            "matches": sum_func(list(self.matched_items.values())),
            # "path": self.path,
            # "parent_path": self.parent_path
        }
        if self.sub_matches:
            subcat = [
                s.summarise(sum_func)
                for s in self.sub_matches
            ]
            subcat.append({
                "unmatched_items": sum_func(self.non_sub_matches)
            })
            rec["categories"] = subcat

        return rec

    def accept(self, visitor):
        visitor.visit(self)
        for s in self.sub_matches:
            s.accept(visitor)


class SubCategoriser(Generic[T], _WithSubCategoriser[T]):
    def __init__(self, name: str, matcher: Callable[[T], bool]) -> None:
        _WithSubCategoriser.__init__(self)
        self.name = name
        self._matcher = matcher

    def __repr__(self) -> str:
        return f"<Cat {self.name}>"

    def has_subcategorisers(self) -> bool:
        return len(self._sub) > 0

    def categorise_list(self, parent_path, path: str, items: Dict[int, T]) -> Optional[ListMatch]:
        matched_items = {
            k: item
            for (k, item) in items.items()
            if self._matcher(item)
        }

        if not matched_items:
            return None

        sub_matched, non_sub_matched = self._sub_categorise_list(parent_path, path, matched_items)
        return ListMatch(self.name, parent_path, path, matched_items, sub_matched, non_sub_matched)


class CategorisedList(NamedTuple):
    nb_items: int
    # Matches from child categories
    category_matches: List["ListMatch"]
    # Items not matched by any categories
    non_category_matches: List[Any]

    def summarise(self, sum_func: Callable[[List[Any]], Any] = len) -> dict:
        """Create a summary of the result

        :param sum_func: function to apply to matching items
        """
        categories = [
            s.summarise(sum_func)
            for s in self.category_matches
        ]
        return {
            "categories": [
                *categories,
                {
                    "unmatched_items": sum_func(self.non_category_matches)
                }
            ]
        }

    def plotly_sankey(self,
                      top_label: str,
                      node_parameters: Optional[dict] = None):
        from .sankey import SankeyVisitor
        visitor = SankeyVisitor("top",
                                nb_items=self.nb_items,
                                nb_unmatched=len(self.non_category_matches),
                                top_label=top_label)
        for s in self.category_matches:
            s.accept(visitor)

        return visitor.get_arguments(node_parameters)


class Categoriser(Generic[T], _WithSubCategoriser[T]):

    def categorise_list(self, items) -> CategorisedList:
        dict_items = dict(enumerate(items))
        list_matches, unmatched = self._sub_categorise_list(None, "top", dict_items)
        return CategorisedList(len(items), list_matches, unmatched)
