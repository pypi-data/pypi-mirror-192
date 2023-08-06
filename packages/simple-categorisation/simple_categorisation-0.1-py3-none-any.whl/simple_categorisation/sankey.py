from typing import Optional

from .simple import ListMatch


class SankeyVisitor:
    def __init__(self, root_path, nb_items: int, nb_unmatched: int, top_label: Optional[str]):
        self.root_path = root_path
        self.nb_items = nb_items
        self.nb_unmatched = nb_unmatched
        self.labels = []
        self.path_to_id = {}
        self._id = self.add_path_and_get_id("node/" + self.root_path, top_label)
        self.source_target_qty = []

        if nb_unmatched > 0:
            un_label = "Unmatched"
            un_path = f"unmatched/{self.root_path}"
            un_target_id = self.add_path_and_get_id(un_path, un_label)
            self.source_target_qty.append((self._id, un_target_id, nb_unmatched))

    def add_path_and_get_id(self, path: str, label: str) -> int:
        new_id = len(self.labels)
        self.path_to_id[path] = new_id
        self.labels.append(label)
        return new_id

    def visit(self, lm: ListMatch):
        label = lm.category_name
        source_id = self.path_to_id["node/" + lm.parent_path]
        target_id = self.add_path_and_get_id("node/" + lm.path, label)
        quantity = len(lm.matched_items)
        self.source_target_qty.append((source_id, target_id, quantity))
        # Unmatched by sub-categories
        if lm.sub_matches:
            un_label = "Unmatched"
            un_source_id = target_id
            un_path = f"unmatched/{lm.path}"
            un_quantity = len(lm.non_sub_matches)
            un_target_id = self.add_path_and_get_id(un_path, un_label)
            self.source_target_qty.append((un_source_id, un_target_id, un_quantity))

    def get_arguments(self, node_parameters: Optional[dict] = None):
        return {
            "node": {
                "label": self.labels,
                **(node_parameters or {}),
            },
            "link": {
                "source": [source for (source, target, qty) in self.source_target_qty],
                "target": [target for (source, target, qty) in self.source_target_qty],
                "value": [qty for (source, target, qty) in self.source_target_qty],
            }
        }
