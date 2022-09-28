## story_1_search_movie_rating_simple    <!-- name of the story - just for debugging -->
* greet
   - utter_greet
* search_movie_rating{"movie": "霸王别姬"}
   - action_search_movie_rating
* bye
   - utter_goodbye

## story_2_search_movie_releasedate_simple
* greet
   - utter_greet
* search_movie_releasedate{"movie": "霸王别姬"}
   - action_search_movie_releasedate
* bye
   - utter_goodbye

## story_3_search_movie_genre_simple
* greet
   - utter_greet
* search_movie_genre{"movie": "霸王别姬"}
   - action_search_movie_genre
* bye
   - utter_goodbye

## story_4_search_movie_introduction_simple
* greet
   - utter_greet
* search_movie_introduction{"movie": "霸王别姬"}
   - action_search_movie_introduction
* bye
   - utter_goodbye

## story_5_search_movie_person_simple
* greet
   - utter_greet
* search_movie_person{"movie": "霸王别姬"}
   - action_search_movie_person
* bye
   - utter_goodbye

## story_6_search_person_biography_simple
* greet
   - utter_greet
* search_person_biography{"person": "巩俐"}
   - action_search_person_biography
* bye
   - utter_goodbye

## story_7_search_person_genre_movie_simple_xyx
* greet
   - utter_greet
* search_person_genre_movie{"person": "巩俐","genre": "恐怖"}
   - action_search_person_genre_movie
* bye
   - utter_goodbye

## story_8_search_person_movie_simple
* greet
   - utter_greet
* search_person_movie{"person": "巩俐"}
   - action_search_person_movie
* bye
   - utter_goodbye

<!-- ## story_9_search_person_person_movie_simple_xyx
* greet
   - utter_greet
* search_person_person_movie{"person": "巩俐"}
   - action_search_person_person_movie
* bye
   - utter_goodbye -->

## story_10_search_person_movie_number_simple
* greet
   - utter_greet
* search_person_movie_number{"person": "巩俐"}
   - action_search_person_movie_number
* bye
   - utter_goodbye

## story_11_search_person_birthday_simple
* greet
   - utter_greet
* search_person_birthday{"person": "巩俐"}
   - action_search_person_birthday
* bye
   - utter_goodbye

## story_120    <!-- to be consistent with domains.yml -->
* first
   - action_first

## story_12
* greet
   - utter_greet
   
## story_13
* bye
   - utter_goodbye

## story_14
* search_movie_rating{"movie": "十面埋伏"}
   - action_search_movie_rating
   
## story_15
* search_movie_releasedate{"movie": "十面埋伏"}
   - action_search_movie_releasedate
   
## story_16
* search_movie_genre{"movie": "十面埋伏"}
   - action_search_movie_genre
   
## story_17
* search_movie_introduction{"movie": "十面埋伏"}
   - action_search_movie_introduction
   
## story_18
* search_movie_person{"movie": "十面埋伏"}
   - action_search_movie_person
   
## story_19
* search_person_biography{"person": "张曼玉"}
   - action_search_person_biography
   
## story_20_xyx
* search_person_genre_movie{"person": "张曼玉"}
   - action_search_person_genre_movie
   
## story_21
* search_person_movie{"person": "张曼玉"}
   - action_search_person_movie
   
<!-- ## story_22_xyx
* search_person_person_movie{"person": "张曼玉"}
   - action_search_person_person_movie -->
   
## story_23
* search_person_movie_number{"person": "张曼玉"}
   - action_search_person_movie_number
   
## story_24
* search_person_birthday{"person": "张曼玉"}
   - action_search_person_birthday
   