from typing import Union
from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from components.slr_parser import SLRParser
from components.grammar import Grammar

app = FastAPI()
app.mount('/static', StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def generate_table(request: Request):
    form = await request.form()
    raw_grammar = form.get("grammar")
    success = False
    error = False
    closure = None
    parse_table = None
    parse_table_symbols = None
    parsing_result = None

    try:
        grammar = Grammar(raw_grammar)
        slr_parser = SLRParser(grammar)
        closure, parse_table, parse_table_symbols = slr_parser.print_info()
        
        results = slr_parser.LR_parser("id + id * id")
        
        body = slr_parser.print_LR_parser(results)
        success = True
        error = False
    except: 
        error = True
        success = False

    slr_parser.generate_automaton()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "grammar": raw_grammar, 
        "error": error,
        "success": success,
        "closure": closure,
        "table": parse_table,
        "symbols": parse_table_symbols,
        "result": body,
    })