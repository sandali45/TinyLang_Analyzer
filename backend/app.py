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

# ---------------------------
# Helpers

