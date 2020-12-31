from SecondCase import FixHalfSpaces,NormalizeCharacters,TokenizeContent,CutStopWords,StemTokens

def NormalizeQuery(query):
    query = FixHalfSpaces(query)
    query = NormalizeCharacters(query)
    query_tokens = TokenizeContent(query)
    query_tokens = CutStopWords(query_tokens)
    query_tokens = StemTokens(query_tokens)
    query_dict = {}
    for token in query_tokens:
        if token not in query_dict.keys():
            query_dict[token] = 1
        else:
            query_dict[token] += 1
    return query_dict

def get_input():
    query = input("Please Enter Your Query:\n\n")
    print("\n", end = '')
    query_dict = NormalizeQuery(query)
    return query_dict



