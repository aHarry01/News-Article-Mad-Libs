import requests
from bs4 import BeautifulSoup
import nltk
import collections as c
import random

#prints the finished madlib with the words replaced with the users input
def print_answer(article, words, user_words):
    for pos in user_words.keys():
        smaller_size = min([len(user_words[pos]),len(words[pos])])
        most_common_words = words[pos].most_common(len(words[pos]))
        rand_words = random.sample(most_common_words, smaller_size)
        if most_common_words[0] in rand_words:
            rand_words.remove(most_common_words[0])
        rand_words.insert(0,most_common_words[0]) #always want to replace the most common word!
        counter = 0
        while (counter < smaller_size):
            article = article.replace(rand_words[counter][0] + " ", user_words[pos][counter].upper() + " ")
            article = article.replace(rand_words[counter][0] + "'s", user_words[pos][counter].upper() + "'s")
            article = article.replace(rand_words[counter][0] + "," , user_words[pos][counter].upper() + ",")
            #print(rand_words[counter][0] + ": " + user_words[pos][counter].upper() + "   ")
            counter += 1
    print(article)

#gets user words to replace the removed words
def get_user_words(words):
    user_words = {}
    for x in words.keys():
        user_words[x] = [input("Enter a(n) " + x + ": ")]
        #get two verbs from the user and three nouns/adjectives
        if x == "noun" or x == "adjective" or x == "verb":
            user_words[x].append(input("Enter another " + x + ": "))
            if x == "noun" or x == "adjective":
                user_words[x].append(input("Enter another " + x + ": "))
    return user_words

#chooses which words that we will replace with user input
def choose_replace_words(article):
    tokens = nltk.word_tokenize(article)
    tagged_words = nltk.pos_tag(tokens)
    words = {"noun": c.Counter(), "proper noun" : c.Counter(), "adjective" : c.Counter(),
             "verb" : c.Counter(), "adverb" : c.Counter(), "past tense verb": c.Counter()}
    #sort words in the parts of speech necessary for a mad lib
    for tagged in tagged_words:
        if len(tagged[0]) != 1 and tagged[0].isalpha() and tagged[0] != "be":
            if tagged[1] == "NN":
                words["noun"][tagged[0]] += 1
            elif tagged[1] == "NNP":
                words["proper noun"][tagged[0]] += 1
            elif tagged[1] == "JJ":
                words["adjective"][tagged[0]] += 1
            elif tagged[1] == "VB": 
                words["verb"][tagged[0]] += 1
            elif tagged[1] == "VBN" or tagged[1] == "VBD":
                words["past tense verb"][tagged[0]] += 1
            elif tagged[1] == "RB":
                words["adverb"][tagged[0]] += 1
    return words

#web scrapes a news article from the associated press
def get_article(all_news_links, index):
    if (index >= len(all_news_links)):
        print("All out of news articles for today!!")
        exit()
    first_news_link = "https://apnews.com" + all_news_links[index]["href"]
    print("Taken from " + first_news_link + '\n')
    r_article = requests.get(first_news_link)
    soup_article = BeautifulSoup(r_article.content, "html.parser")
    article_info = soup_article.find("div", {"data-key" : "article"}).find_all('p')
    article = ""
    for paragraph in article_info:
        article += paragraph.get_text() + '\n\n'
    return article

#gets the list of links to news articles on the website
def get_news_links():
    r1 = requests.get("https://apnews.com/")
    soup = BeautifulSoup(r1.content, "html.parser")
    all_news_links = soup.find_all('a', {"data-key" : "story-link"} )
    return all_news_links

news_links = get_news_links()
cont = True
count = 0
#main loop - loop until user quits program
while (cont):
    article = get_article(news_links, count)
    count += 1
    words = choose_replace_words(article)
    user_words = get_user_words(words)
    print_answer(article, words, user_words)
    a = input("Another madlib? [y/n] ")
    if a == 'n' or a == 'N':
        cont = False
