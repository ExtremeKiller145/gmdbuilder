#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class Node:
    name: str
    member_lines: List[str] = field(default_factory=list)
    children: Dict[str, "Node"] = field(default_factory=dict)


IMPORT_LINE_RE = re.compile(r"^\s*(from\s+|import\s+)")
BAD_CLASS_CHARS_RE = re.compile(r"[^A-Za-z0-9_]")
SPLIT_WORDS_RE = re.compile(r"[^A-Za-z0-9]+")


def is_pycache(p: Path) -> bool:
    return p.is_dir() and p.name == "__pycache__"


def to_class_name(raw: str) -> str:
    words = [w for w in SPLIT_WORDS_RE.split(raw.strip()) if w]
    if not words:
        words = ["Generated"]
    name = "".join(w[:1].upper() + w[1:] for w in words)
    if name[0].isdigit():
        name = "N" + name
    name = BAD_CLASS_CHARS_RE.sub("_", name)
    if not name.isidentifier():
        name = "_" + name
    return name




def collect_member_lines(py_text: str, prefix: str) -> List[str]:
    lines: List[str] = []
    for line in py_text.splitlines():
        if IMPORT_LINE_RE.match(line):
            continue
        if "=" in line:
            lines.append(line.rstrip())
    return lines


def build_tree_for_dir(root_class: str, top_path: Path, prefix: str) -> Node:
    root = Node(name=root_class)

    def walk_dir(dir_path: Path, node: Node) -> None:
        init_file = dir_path / "__init__.py"
        if init_file.exists():
            node.member_lines.extend(
                collect_member_lines(init_file.read_text(encoding="utf-8", errors="replace"), prefix)
            )

        for child in sorted(dir_path.iterdir(), key=lambda p: p.name):
            if child.name.startswith(".") or is_pycache(child):
                continue

            if child.is_dir():
                cnode = Node(name=to_class_name(child.name))
                node.children[cnode.name] = cnode
                walk_dir(child, cnode)

            elif child.is_file() and child.suffix == ".py" and child.name != "__init__.py":
                cnode = Node(name=to_class_name(child.stem))
                cnode.member_lines.extend(
                    collect_member_lines(child.read_text(encoding="utf-8", errors="replace"), prefix)
                )
                node.children[cnode.name] = cnode

    def walk_file(py_file: Path, node: Node) -> None:
        node.member_lines.extend(
            collect_member_lines(py_file.read_text(encoding="utf-8", errors="replace"), prefix)
        )

    if top_path.is_dir():
        walk_dir(top_path, root)
    else:
        walk_file(top_path, root)

    return root


def emit(node: Node, indent: int = 0) -> str:
    sp = " " * indent
    out: List[str] = []
    out.append(f"{sp}class {node.name}(str):")
    if node.member_lines:
        for ln in node.member_lines:
            out.append(f"{sp}    {ln}")
    else:
        out.append(f"{sp}    pass")
    for child_name in sorted(node.children.keys()):
        out.append("")
        out.append(emit(node.children[child_name], indent + 4))
    return "\n".join(out)


def write_out(dest_dir: Path, filename_stem: str, root: Node) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_path = dest_dir / f"{filename_stem}.py"
    content = "from enum import Enum\n\n" + emit(root) + "\n"
    out_path.write_text(content, encoding="utf-8")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source_dir", type=Path)
    ap.add_argument("dest_dir", type=Path)
    ap.add_argument("--prefix", default="a", help='Prefix for int keys (default: "a")')
    args = ap.parse_args()

    src: Path = args.source_dir
    dst: Path = args.dest_dir
    prefix: str = args.prefix

    if not src.exists() or not src.is_dir():
        raise SystemExit(f"Source directory does not exist or is not a directory: {src}")

    for child in sorted(src.iterdir(), key=lambda p: p.name):
        if child.name.startswith(".") or is_pycache(child):
            continue

        if child.is_dir():
            tree = build_tree_for_dir(to_class_name(child.name), child, prefix)
            out_file = write_out(dst, child.name, tree)
            print(f"Wrote: {out_file}")

        elif child.is_file() and child.suffix == ".py" and child.name != "__init__.py":
            tree = build_tree_for_dir(to_class_name(child.stem), child, prefix)
            out_file = write_out(dst, child.stem, tree)
            print(f"Wrote: {out_file}")

    print("Done.")


if __name__ == "__main__":
    main()
