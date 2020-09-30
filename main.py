#!/usr/bin/python3

from stackexchange import query_questions

print(query_questions('vi', tagged=["vim", "autocmd"]))
