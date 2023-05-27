"""
Search index (main) view.

URLs include:
/
"""

import heapq
import threading
import flask
import requests
import search


def search_thread(url, result):
    """Map 2."""
    return_json = None
    response = requests.get(url, timeout=15)

    if response.status_code == 200:
        return_json = response.json()
    if return_json:
        result.append(return_json["hits"][0:10])
    # [{doc_id:123, score: 100}, ...]


@search.app.route('/', methods=['GET'])
def show_index():
    """Map 2."""
    # getting q and w start ^_^
    d_style = {}
    q_q = flask.request.args.get("q", default=None)
    w_w = flask.request.args.get("w")
    if q_q is None:
        return flask.render_template("index.html")
    # q = flask.request.args.get("q")
    q_q = q_q.strip().replace(" ", "+")
    if w_w is None:
        w_w = "0.5"
    # getting q and w end ^_^
    overall_results = []
    d_style["threads"] = []
    # threads = []
    # composing the url and send the url to three different servers
    # path = search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]
    for p_p in search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]:
        # url = p_p + "?q=" + q_q + "&w=" + w_w
        single_search_thread = threading.Thread(
            target=search_thread, args=(p_p + "?q=" + q_q + "&w=" + w_w,
                                        overall_results))
        d_style["threads"].append(single_search_thread)
        single_search_thread.start()

    for t_t in d_style["threads"]:
        t_t.join()

    # getting combined results from all servers and getting the ten with
    # highest score
    def func(d_d):
        """Map 2."""
        return d_d["score"]
    # merged_results = heapq.merge(*overall_results, key=func)
    sorted_results = sorted(heapq.merge(*overall_results, key=func),
                            key=func, reverse=True)
    first_ten_docid = []
    d_style["length_return"] = 0
    # length_return = 0
    if len(sorted_results) >= 10:
        d_style["length_return"] = 10
    else:
        d_style["length_return"] = len(sorted_results)
    for i in range(d_style["length_return"]):
        first_ten_docid.append(int(sorted_results[i]["docid"]))
    context = {}
    d_style["docs_list"] = []
    # docs_list = []
    for doc_id in first_ten_docid:
        return_documents = search.model.get_db().execute(
            "SELECT * "
            # here the name after front should be the name of a table
            # from the database
            "FROM Documents "
            "WHERE docid == ?",
            (doc_id,)
        ).fetchone()
        # print(return_documents)
        doc_info = {}
        # (docid,title,summary,url)
        doc_info["url"] = return_documents["url"]
        if doc_info["url"] == '':
            doc_info["url"] = "No url available"
        doc_info["title"] = return_documents["title"]
        doc_info["summary"] = return_documents["summary"]
        if doc_info["summary"] == '':
            doc_info["summary"] = "No summary available"
        d_style["docs_list"].append(doc_info)
    context = {"docs": d_style["docs_list"]}
    q_q = q_q.replace("+", " ")
    context["query_term"] = q_q
    context["weight"] = w_w
    return flask.render_template("index.html", **context)
