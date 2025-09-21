# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from lark import Lark, Token, Tree, UnexpectedInput
from graphviz import Digraph
import os
from fastapi.staticfiles import StaticFiles
app = FastAPI(title="TinyLang Analyzer")

# ---------------------------
# Serve frontend folder
# ---------------------------
from fastapi.staticfiles import StaticFiles
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def root():
    index_file = os.path.join(frontend_path, "index.html")
    return FileResponse(index_file)

# ---------------------------
# Enable CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Grammar (TinyLang)
# ---------------------------
GRAMMAR = r"""
start: stmt*

?stmt: declaration
    | assign ";"
    | print_stmt ";"
    | if_stmt
    | while_stmt

declaration: "int" NAME ";"    -> declaration
assign: NAME "=" expr          -> assign
print_stmt: "print" "(" expr ")"  -> print_stmt

if_stmt: "if" "(" expr ")" block ("else" block)?  -> if_stmt
while_stmt: "while" "(" expr ")" block            -> while_stmt
block:  "{" stmt* "}"

?expr: expr "+" term           -> add
    | expr "-" term           -> sub
    | expr ">" term           -> gt
    | expr "<" term           -> lt
    | expr ">=" term          -> ge
    | expr "<=" term          -> le
    | expr "==" term          -> eq
    | expr "!=" term          -> ne
    | term

?term: term "*" factor         -> mul
    | term "/" factor          -> div
    | term "%" factor          -> mod
    | factor

?factor: NUMBER                -> number
      | NAME                  -> var
      | "(" expr ")"

%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS
%ignore WS
COMMENT: /\/\/[^\n]*/
%ignore COMMENT
"""

parser = Lark(GRAMMAR, parser="lalr", propagate_positions=True)

# ---------------------------
# Request/Response Models
# ---------------------------
class AnalyzeRequest(BaseModel):
    source: str

class TokenOut(BaseModel):
    type: str
    value: str
    line: Optional[int] = None
    column: Optional[int] = None

class ErrorOut(BaseModel):
    kind: str
    message: str
    line: Optional[int] = None
    column: Optional[int] = None

class AnalyzeResponse(BaseModel):
    tokens: List[TokenOut]
    errors: List[ErrorOut]
    tree: Dict[str, Any]
    svg: str


def tokens_only(text: str) -> List[Token]:
    return list(parser.lex(text))

def tree_to_json(t: Tree) -> Dict[str, Any]:
    def walk(n, idx=0):
        if isinstance(n, Tree):
            node = {"id": f"n{idx}", "label": n.data, "children": []}
            next_idx = idx + 1
            for c in n.children:
                child, next_idx = walk(c, next_idx)
                node["children"].append(child)
            return node, next_idx
        else:
            node = {"id": f"n{idx}", "label": f"{n.type}:{str(n)}", "children": []}
            return node, idx + 1
    root, _ = walk(t, 0)
    return root

def tree_to_svg(t: Tree) -> str:
    dot = Digraph("ParseTree", format="svg")
    counter = [0]
    def add(n):
        nid = f"n{counter[0]}"
        counter[0] += 1
        if isinstance(n, Tree):
            dot.node(nid, n.data, shape="ellipse")
            for ch in n.children:
                cid = add(ch)
                dot.edge(nid, cid)
        else:
            dot.node(nid, f"{n.type}\n{str(n)}", shape="box")
        return nid
    add(t)
    svg_bytes = dot.pipe(format="svg")
    return svg_bytes.decode("utf-8")
def _format_syntax_error(e: UnexpectedInput, text: str) -> ErrorOut:
    expected = None
    try:
        if getattr(e, "expected", None):
            expected = ", ".join(sorted(e.expected))
    except Exception:
        expected = None
    snippet = None
    try:
        snippet = e.get_context(text, span=60)
    except Exception:
        snippet = None
    parts = ["Syntax error."]
    if expected:
        parts.append(f"Expected one of: {expected}.")
    if snippet:
        parts.append("Here:\n" + snippet)
    return ErrorOut(
        kind="syntax",
        message=" ".join(parts) if expected else (parts[0] + ("\n" + snippet if snippet else "")),
        line=getattr(e, "line", None),
        column=getattr(e, "column", None),
    )
