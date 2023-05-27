"""Index REST API."""
import os
import re
import math
import flask
import index

# GET /api/v1/


@index.app.route('/api/v1/', methods=['GET'])
def return_service():
    """Index REST API."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context), 200

# GET /api/v1/hits/query
# http "localhost:9000/api/v1/hits/?q=university+michigan&w=1.0"


@index.app.route("/api/v1/hits/", methods=['GET'])
def return_services():
    """Index REST API."""
    query = flask.request.args.get("q", type=str)
    # getting query list and weight from client
    query = query_processing(query)
    weight = flask.request.args.get("w", default=0.5, type=float)
    # print(query)
    doc_score_list = get_calculation_result(query, weight)
    hit_list = []
    if len(doc_score_list) == 0:
        context = {
            "hits": hit_list
        }
        return flask.jsonify(**context), 200
    for doc_score in doc_score_list:
        if doc_score[1] == 0.0:
            continue
        one_result = {"docid": doc_score[0], "score": doc_score[1]}
        hit_list.append(one_result)
    context = {
        "hits": hit_list
    }
    return flask.jsonify(**context), 200


def get_calculation_result(query, weight):
    """Index REST API."""
    pagerank = index.app.config["PAGERANK_DICT"]
    query_vector = get_query_vector(query)
    if len(query_vector) == 0:
        return []
    overall_document_vector = get_document_vector(query)
    doc_score = []
    # overall_document_vector: {doc_id:[tf_apple * idfk_apple,]}
    for doc_id, document_vector in overall_document_vector.items():
        # document_vector -->  # [doc_id:[tf_apple * idfk_apple,]]
        q_dot_product_di = dot_product(query_vector, document_vector)
        q_hat = float(normal_factor(query_vector))
        # working on this -_-
        d_hat = math.sqrt(float(index.app.config["DI_DICT"][doc_id]))
        tf_idf = float(float(q_dot_product_di) / float((q_hat * d_hat)))
        score = float(float(weight) * pagerank[doc_id] + (1-weight) * tf_idf)
        doc_score.append([doc_id, score])
    doc_score = sorted(doc_score, key=lambda x: x[1], reverse=True)
    return doc_score


def normal_factor(query_vector):
    """Index REST API."""
    result = 0
    l_l = len(query_vector)
    for i in range(l_l):
        result += float(query_vector[i] ** 2)
    return float(math.sqrt(result))


def dot_product(query_vector, document_vector):
    """Index REST API."""
    result = 0
    l_l = len(query_vector)
    for i in range(l_l):
        result += query_vector[i] * document_vector[i]
    return result


def get_query_vector(query):
    """Index REST API."""
    index_dict = index.app.config["INDEX_DICT"]
    query_vec = []
    already_add = {}
    for word in query:
        if word in already_add:
            continue
        if word in index_dict:
            current_idfk = index_dict[word][0]
            current_tfik = query.count(word)
            result = float(current_idfk * current_tfik)
            query_vec.append(result)
            already_add[word] = 1
        # if query is not in all output document not only one document
        else:
            query_vec = []
            break
    return query_vec


def get_document_vector(query):
    """Index REST API."""
    doc_dict = index.app.config["DOC_DICT"]
    index_dict = index.app.config["INDEX_DICT"]
    # {doc_id:[tf_apple * idfk_apple,]}
    doc_vector_dict = {}
    result = 0
    # *_*
    # key doc_id value: occurrence of the doc_id
    docid_dic = {}
    for word in query:
        counter = 0
        for info_list in index_dict[word]:
            if counter == 0:
                counter += 1
                continue
            doc_id = info_list[0]
            if doc_id not in docid_dic:
                docid_dic[doc_id] = 0
            docid_dic[doc_id] += 1
    new_docid_dic = {key: val for key,
                     val in docid_dic.items() if val == len(query)}
    for doc_id in new_docid_dic:
        # 三个搜索词都出现的情况
        if docid_dic[doc_id] == len(query):
            for word in query:
                info = doc_dict[doc_id][word]
                idfk, tfik, _ = info
                result = idfk * tfik
                if doc_id not in doc_vector_dict:
                    doc_vector_dict[doc_id] = []
                doc_vector_dict[doc_id].append(result)
    return doc_vector_dict


def query_processing(query):
    """Index REST API."""
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    word_list = text.casefold().strip().split()
    filtered_list = []
    stopwords = index.app.config["STOPWORD"]
    for word in word_list:
        if word not in stopwords:
            filtered_list.append(word)
    return filtered_list


def load_index():
    """Index REST API."""
    d_style = {}
    di_dict = {}
    # Load pagerank into memory
    pagerank_dict = {}
    d_style["doc_dict"] = {}
    # doc_dict = {}
    index_dict = {}
    with open(os.path.join(
        index.app.root_path, index.app.config["PAGERANK_FILE"]),
            'r', encoding="utf-8") as f_f:
        for line in f_f:
            key, value = line.strip().split(",")
            pagerank_dict[int(key)] = float(value)
    index.app.config["PAGERANK_DICT"] = pagerank_dict
    # Load stopwords
    d_style["stopwords"] = []
    # stopwords = []
    with open(os.path.join(
        index.app.root_path, index.app.config["STOPWORD_FILE"]), "r",
            encoding="utf-8") as stopword:
        d_style["stopwords"] = stopword.read().strip().split()
    index.app.config["STOPWORD"] = d_style["stopwords"]
    # Load inverted index
    with open(os.path.join(
        index.app.root_path, 'inverted_index',
            index.app.config["INDEX_PATH"]), "r",
                encoding="utf-8") as file_index:
        for line in file_index:
            var_list = line.split()
            word = var_list[0]
            index_dict[word] = []
            idfk = float(var_list[1])
            index_dict[word].append(idfk)
            doc_num = (len(var_list) - 2) // 3
            var_list.pop(0)
            var_list.pop(0)

            for i in range(0, doc_num):
                # [doc_id,tfik,|di|]
                # d_i = float(var_list[i * 3 + 2])
                index_dict[word].append([int(var_list[i * 3]),
                                        int(var_list[i * 3 + 1]),
                                        float(var_list[i * 3 + 2])])
                if int(var_list[i * 3]) not in d_style["doc_dict"]:
                    d_style["doc_dict"][int(var_list[i * 3])] = {}
                d_style["doc_dict"][int(var_list[i * 3])][
                    word] = [idfk, int(var_list[i * 3 + 1]),
                             float(var_list[i * 3 + 2])]
                di_dict[int(var_list[i * 3])] = float(var_list[i * 3 + 2])

    index.app.config["DOC_DICT"] = d_style["doc_dict"]
    index.app.config["INDEX_DICT"] = index_dict
    index.app.config["DI_DICT"] = di_dict
