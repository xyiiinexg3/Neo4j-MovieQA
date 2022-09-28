# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


import sys
import logging
import re
from typing import Text, Dict, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from py2neo import Graph
from markdownify import markdownify as md

logger = logging.getLogger(__name__)

# 1.获取电影名列表 xyx
p = 'data/lookup/newmovie_v4.txt'
movie_names = [i.strip() for i in open(p, 'r', encoding='UTF-8').readlines()]
# default neo4j account should be user="neo4j", password="neo4j"
try:
    graph = Graph(host="127.0.0.1", http_port=7474, user="neo4j", password="123456") # xyx
except Exception as e:
    logger.error('Neo4j connection error: {}, check your Neo4j'.format(e))
    sys.exit(-1)
else:
    logger.debug('Neo4j Database connected successfully.')

# 2.利用正则表达式 xyx
def retrieve_movie_name(name):
    names = []
    name = '.*' + '.*'.join(list(name)) + '.*'
    pattern = re.compile(name) # compile编译正则表达式，生成pattern对象
    for i in movie_names:
        candidate = pattern.search(i) # pattern.search(S)就是在字符串S中寻找匹配之前生成pattern的子串
        if candidate:
            names.append(candidate.group()) # m.group() == m.group(0) == 所有匹配的字符
    return names

# 3.暂时不懂作用是啥
def make_button(title, payload):
    return {'title': title, 'payload': payload}

# 4.action
class ActionEcho(Action):
    def name(self) -> Text:
        return "action_echo"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        user_say = "You said: " + tracker.latest_message['text']
        dispatcher.utter_message(user_say)
        return []

# xyx
class ActionFirst(Action):
    def name(self) -> Text:
        return "action_first"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        # dispatcher.utter_template("utter_first", tracker)
        # print('ActionFirst'*10)
        dispatcher.utter_message(template="utter_first")
        # dispatcher.utter_template("utter_howcanhelp", tracker)
        # print('dispatcher.utter_message')
        dispatcher.utter_message(md("您可以这样向我提问: <br/>霸王别姬<br/>\
                              霸王别姬是什么类型的电影<br/>\
                              霸王别姬的上映时间<br/>\
                              霸王别姬的演员有哪些人<br/>\
                              巩俐是谁<br/>\
                              巩俐的出生日期<br/>\
                              巩俐演了多少部电影<br/>\
                              巩俐演了哪些电影<br/>\
                              巩俐有演过的剧情电影1"))                              
        return []

# xyx
class ActionDonKnow(Action):
    def name(self) -> Text:
        return "action_donknow"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        # dispatcher.utter_template("utter_donknow", tracker)
        dispatcher.utter_message(template="utter_donknow")
        # dispatcher.utter_template("utter_howcanhelp", tracker)
        dispatcher.utter_message(md("您可以这样向我提问: <br/>霸王别姬<br/>\
                              霸王别姬是什么类型的电影<br/>\
                              霸王别姬的上映时间<br/>\
                              霸王别姬的演员有哪些人<br/>\
                              巩俐是谁<br/>\
                              巩俐的出生日期<br/>\
                              巩俐演了多少部电影<br/>\
                              巩俐演了哪些电影<br/>\
                              巩俐有演过的剧情电影2"))     
        return []

# 1.action_search_movie_rating
class ActionSearchMovieRating(Action):
    def name(self) -> Text:
        return "action_search_movie_rating"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        movie = tracker.get_slot("movie")
        pre_movie = tracker.get_slot("sure")
        print("pre_movie::::" + str(pre_movie))
        
        possible_movies = retrieve_movie_name(movie)
        # if len(possible_diseases) == 1 or sure == "true":

        if movie == pre_movie or len(possible_movies) == 1:
            a = graph.run("match (a:Movie{title: {movie}}) return a", movie=movie).data()[0]['a']
            if "rating" in a:
                rating = a['rating']
                template = "{0}的电影评分：{1}"
                retmsg = template.format(movie, rating)
            else:
                retmsg = movie + "暂无其评分的信息"
            dispatcher.utter_message(retmsg)
            # if "treat" in a:
            #     treat = a['treat']
            #     template = "{0}的治疗方式有：{1}"
            #     retmsg = template.format(disease, "、".join(treat))
            # else:
            #     retmsg = disease + "暂无常见治疗方式"
            # dispatcher.utter_message(retmsg)

        # 5.进一步确定疾病类型，但电影好像不需要这个 xyx 
        # 需要！！！在确定电影名的时候有系列，比如哈利波特1，2，3
        elif len(possible_movies) > 1:
            buttons = []
            for d in possible_movies:
                # 有疑问 xyx sure是干嘛的
                buttons.append(make_button(d, '/search_movie_rating{{"movie":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的电影，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 电影相关的记录".format(movie))
        return []

# 2.xyx action_search_movie_releasedate
class ActionSearchMovieReleaseDate(Action):
    def name(self) -> Text:
        return "action_search_movie_releasedate"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        movie = tracker.get_slot("movie")
        # 
        pre_movie = tracker.get_slot("sure")
        print("pre_movie::::" + str(pre_movie))
        
        possible_movies = retrieve_movie_name(movie)
        """ search_movie_releasedate db action here """
        # food = dict()
        if movie == pre_movie or len(possible_movies) == 1:
            # m = [x['m.name'] for x in graph.run("match (a:Disease{name: {disease}})-[:can_eat]->(m:Food) return m.name",
            #               disease=disease).data()]
            # food['can_eat'] = "、".join(m) if m else "暂无记录"

            # m = [x['m.name'] for x in graph.run("match (a:Disease{name: {disease}})-[:not_eat]->(m:Food) return m.name",
            #               disease=disease).data()]

            # food['not_eat'] = "、".join(m) if m else "暂无记录"

            # retmsg = "在患 {0} 期间，可以食用：{1}，\n但不推荐食用：{2}".\
            #                 format(disease, food['can_eat'], food['not_eat'])
            a = graph.run("match (a:Movie{title: {movie}}) return a", movie=movie).data()[0]['a']

            if "releasedate" in a:
                releasedate = a['releasedate']
                template = "{0}的首映时间：{1}"
                retmsg = template.format(movie, releasedate)
            else:
                retmsg = movie + "暂无其首映时间的信息"
            dispatcher.utter_message(retmsg)
        elif len(possible_movies) > 1:
            buttons = []
            for d in possible_movies:
                # 有疑问 xyx sure是干嘛的
                buttons.append(make_button(d, '/search_movie_releasedate{{"movie":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的电影，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 电影相关的记录".format(movie))
        return []

# 3.xyx action_search_movie_genre
class ActionSearchMovieGenre(Action):
    def name(self) -> Text:
        return "action_search_movie_genre"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        movie = tracker.get_slot("movie")
        # premovie不知道是干嘛的
        pre_movie = tracker.get_slot("sure")
        print("pre_movie::::" + str(pre_movie))
        
        possible_movies = retrieve_movie_name(movie)
        if movie == pre_movie or len(possible_movies) == 1:
            # a = [x['s.name'] for x in graph.run("MATCH (p:Disease{name: {disease}})-[r:has_symptom]->\
            #                                     (s:Symptom) RETURN s.name", disease=disease).data()]
            # template = "{0}的症状可能有：{1}"
            # retmsg = template.format(disease, "、".join(a))
            # dispatcher.utter_message(retmsg)

            # 电影1：m体裁一对多，需要通过关系查询 xyx
            cql = f"match(m:Movie)-[r:is]->(b) where m.title='{movie}' return b.name"

            b = [x['b.name'] for x in graph.run(cql).data()]

            template = "{0}是{1}等类型的电影"
            retmsg = template.format(movie, "、".join(b))

            # m = [x['m.name'] for x in graph.run("match (a:Disease{name: {disease}})-[:can_eat]->(m:Food) return m.name",
            #               disease=disease).data()]
            # food['can_eat'] = "、".join(m) if m else "暂无记录"

            # if "genre" in a:
            #     genre = a['genre']
            #     template = "{0}的体裁类型：{1}"
            #     retmsg = template.format(movie, genre)
            # else:
            #     retmsg = movie + "暂无其体裁类型的信息"


            dispatcher.utter_message(retmsg)

        elif len(possible_movies) > 1:
            buttons = []
            for d in possible_movies:
                # 有疑问 xyx sure是干嘛的
                buttons.append(make_button(d, '/search_movie_genre{{"movie":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的电影，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 电影相关的记录".format(movie))

        return []

# 4.xyx action_search_movie_introduction
class ActionSearchMovieIntroduction(Action):
    def name(self) -> Text:
        return "action_search_movie_introduction"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        movie = tracker.get_slot("movie")
        pre_movie = tracker.get_slot("sure")
        print("pre_movie::::" + str(pre_movie))
        
        possible_movies = retrieve_movie_name(movie)
        if movie == pre_movie or len(possible_movies) == 1:
            # a = graph.run("match (a:Disease{name: {disease}}) return a.cause", disease=disease).data()[0]['a.cause']
            # if "treat" in a:
            #     treat = a['treat']
            #     template = "{0}的治疗方式有：{1}"
            #     retmsg = template.format(disease, "、".join(treat))
            # else:
            #     retmsg = disease + "暂无该疾病的病因的记录"

            # dispatcher.utter_message(retmsg)

            a = graph.run("match (a:Movie{title: {movie}}) return a", movie=movie).data()[0]['a']

            if "introduction" in a:
                introduction = a['introduction']
                template = "{0}的剧情介绍：{1}"
                retmsg = template.format(movie, introduction)
            else:
                retmsg = movie + "暂无其剧情介绍的信息"
            dispatcher.utter_message(retmsg)

        elif len(possible_movies) > 1:
            buttons = []
            for d in possible_movies:
                # 有疑问 xyx sure是干嘛的
                buttons.append(make_button(d, '/search_movie_introduction{{"movie":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的电影，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 电影相关的记录".format(movie))

        return []

# 5. xyx action_search_movie_person  waiting----------8.14.2022
class ActionSearchMoviePerson(Action):
    def name(self) -> Text:
        return "action_search_movie_person"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        movie = tracker.get_slot("movie")
        pre_movie = tracker.get_slot("sure")
        print("pre_movie::::" + str(pre_movie))
        
        possible_movies = retrieve_movie_name(movie)
        if movie == pre_movie or len(possible_movies) == 1:
            cql = f"match(n:Person)-[r:actedin]->(m:Movie) where m.title='{movie}' return n.name"
            
            a = [x['n.name'] for x in graph.run(cql).data()]
            template = "{0}由{1}等演员主演"
            retmsg = template.format(movie, "、".join(a))
            dispatcher.utter_message(retmsg)
        elif len(possible_movies) > 1:
            buttons = []
            for d in possible_movies:
                buttons.append(make_button(d, '/search_movie_person{{"movie":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的电影，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 电影相关的信息".format(movie))
        return []

# 6.xyx action_search_person_biography
class ActionSearchPersonBiography(Action):
    def name(self) -> Text:
        return "action_search_person_biography"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        person = tracker.get_slot("person")
        # pre_person = tracker.get_slot("sure")
        # print("pre_movie::::" + str(pre_movie))
        
        # possible_movies = retrieve_movie_name(movie)
        # if movie == pre_movie or len(possible_movies) == 1:
        if person:
            cql = f"match(n:Person)-[]->() where n.name='{person}' return n.biography"

            a = graph.run(cql).data()[0]['n.biography']
            # if a:
            #     template = "在患 {0} 时，可能会用药：{1}"
            #     retmsg = template.format(disease, "、".join(a))
            # else:
            #     retmsg = "无 %s 的可能用药记录" % disease

            template = "演员 {0} 的介绍：{1}"
            retmsg = template.format(person, a)
            dispatcher.utter_message(retmsg)

        # elif len(possible_diseases) > 1:
        #     buttons = []
        #     for d in possible_diseases:
        #         buttons.append(make_button(d, '/search_drug{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
        #     dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 演员相关的记录".format(person))
        return []

# 7. xyx action_search_person_genre_movie
class ActionSearchPersonGenreMovie(Action):
    def name(self) -> Text:
        return "action_search_person_genre_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        
        person = tracker.get_slot("person")
        genre = tracker.get_slot("genre")
        # 查询电影名称
        cql = f"match(n:Person)-[]->(m:Movie) where n.name='{person}' return m.title"
        print(cql)
        movie_name_list = list(graph.run(cql).data())
        print(movie_name_list)
        # 查询类型
        result = []
        for movie_name in movie_name_list:
            print(movie_name['m.title'])
            movie_name = movie_name['m.title'].strip() # 这里的[0]应该相当于['m.title']
            print(movie_name)
            try:
                cql = f"match(m:Movie)-[r:is]->(t) where m.title='{movie_name}' return t.name"
                print(cql)
                temp_type = []
                temp = list(graph.run(cql).data())
                for t in temp:
                    temp_type.append(t['t.name']) # [0] = ['t.name']
                print(temp_type)
                if len(temp_type) == 0:
                    continue
                if genre in temp_type:
                    result.append(movie_name)
            except:
                continue
        #print(result)
        if len(result): # 有答案的话
            answers = "、".join(result)
            retmsg = person + "演过的" + genre + "电影有:\n" + answers + "。"
            dispatcher.utter_message(retmsg)
        
        
        # disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        # print("pre_disease::::" + str(pre_disease))
        
        # possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        #     a = graph.run("match (a:Disease{name: {disease}}) return a.prevent", disease=disease).data()[0]
        #     if 'a.prevent' in a:
        #         prevent = a['a.prevent']
        #         template = "以下是有关预防 {0} 的知识：{1}"
        #         retmsg = template.format(disease, md(prevent.replace('\n', '<br/>')))
        #     else:
        #         retmsg = disease + "暂无常见预防方法"
        #     dispatcher.utter_message(retmsg)
        # elif len(possible_diseases) > 1:
        #     buttons = []
        #     for d in possible_diseases:
        #         buttons.append(make_button(d, '/search_prevention{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
        #     dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与演员 {0} 表演 {1} 体裁相关的电影记录".format(person, genre))
        return []

# 8.xyx action_search_person_movie
class ActionSearchPersonMovie(Action):
    def name(self) -> Text:
        return "action_search_person_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        person = tracker.get_slot("person")
        if person:
            cql = f"match(n:Person)-[]->(m:Movie) where n.name='{person}' return m.title"

            a = [x['m.title'] for x in graph.run(cql).data()]
            template = "{0} 演过 {1} 等电影"
            retmsg = template.format(person, "、".join(a))
        else:
            retmsg = "知识库中暂无与演员 {0} 参演的电影记录".format(person)

        dispatcher.utter_message(retmsg)
        return []
'''
# 9.xyx action_search_person_person_movie
class ActionSearchPersonPersonMovie(Action):
    def name(self) -> Text:
        return "action_search_person_person_movie" # treat_period

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))
        
        possible_diseases = retrieve_disease_name(disease)
        if disease == pre_disease or len(possible_diseases) == 1:
            a = graph.run("match (a:Disease{name: {disease}}) return a", disease=disease).data()[0]['a']
            if "treat_period" in a:
                treat_period = a['treat_period']
                template = "{0}需要的治疗时间：{1}"
                retmsg = template.format(disease, treat_period)
            else:
                retmsg = disease + "暂无治疗时间的记录"
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_disease_treat_time{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 相关的治疗时间记录".format(disease))
        return []
'''

# 10. action_search_person_movie_number
class ActionSearchPersonMovieNumber(Action):
    def name(self) -> Text:
        return "action_search_person_movie_number"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        # person = tracker.get_slot("person")
        # pre_person = tracker.get_slot("sure")
        # print("pre_person::::" + str(pre_disease))
        
        # possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        #     a = graph.run("match (a:Disease{name: {disease}}) return a", disease=disease).data()[0]['a']
        #     easy_get = a['easy_get']
        #     template = "{0}的易感人群是：{1}"
        #     retmsg = template.format(disease, easy_get)
        #     dispatcher.utter_message(retmsg)
        # elif len(possible_diseases) > 1:
        #     buttons = []
        #     for d in possible_diseases:
        #         buttons.append(make_button(d, '/search_easy_get{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
        #     dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 相关的易感人群记录".format(disease))
        
        person = tracker.get_slot("person")
        if person:
            cql = f"match(n:Person)-[]->(m:Movie) where n.name='{person}' return m.title"

            # a = [x['m.title'] for x in graph.run(cql).data()]
            b = len(graph.run(cql).data())
            template = "{0} 演过 {1} 部电影"
            retmsg = template.format(person, b)
        else:
            retmsg = "知识库中暂无与演员 {0} 参演电影数目的记录".format(person)

        dispatcher.utter_message(retmsg)

        return []

# 11. action_search_person_birthday
class ActionSearchPersonBirthday(Action):
    def name(self) -> Text:
        return "action_search_person_birthday"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        # disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        # print("pre_disease::::" + str(pre_disease))
        
        # possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        #     a = graph.run("match (a:Disease{name: {disease}})-[:belongs_to]->(s:Department) return s.name",
        #                   disease=disease).data()[0]['s.name']
        #     template = "{0} 属于 {1}"
        #     retmsg = template.format(disease, a)
        #     dispatcher.utter_message(retmsg)
        # elif len(possible_diseases) > 1:
        #     buttons = []
        #     for d in possible_diseases:
        #         buttons.append(make_button(d, '/search_disease_dept{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
        #     dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 疾病相关的科室记录".format(disease))
        
        person = tracker.get_slot("person")
        if person:
            cql = f"match(n:Person)-[]->() where n.name='{person}' return n.birth"

            a = graph.run(cql).data()[0]['n.birth']
            # b = len(graph.run(cql).data())
            template = "{0} 的生日是 {1} "
            retmsg = template.format(person, a)
        else:
            retmsg = "知识库中暂无与演员 {0} 生日的记录".format(person)

        dispatcher.utter_message(retmsg)

        return []
