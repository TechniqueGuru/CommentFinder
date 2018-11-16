import praw

username = ""

reddit = praw.Reddit(client_id="", client_secret="",
                     username="", password="",
                     user_agent="")

ask_check = "n"
name = False

while True:
    if ask_check == "n":
        name_check = input("Would you like to use the same username every query? (Y/N) (Def:Y): ")
        ask_check = "y"

    name_check = name_check.lower()
    if name_check == "" or name_check == "yes":
        name_check = "y"
    if name_check != "y" or name == False:
        name = input("Enter username: ")

    if name == "":
        print(f"No username was entered. Using preset username: \"{username}\".")
        name = username

    search = ""
    while search == "":
        search = input("Search phrase (You can search for multiple terms, serparting them using a comma ','): ")

    inclusive = input("Would you like to find comments containing all the search phrases (Y)? Or search for each term separately (N)? (Def: N): ")
    inclusive = inclusive.lower()
    if inclusive == "":
        print("No input for comment inclusivity. Using default setting (N).")
        inclusive = "n"
    if inclusive == "no":
        inclusive = "n"
    if inclusive == "yes":
        inclusive = "y"
    if inclusive != "n" and inclusive != "y":
        print("Invalid input for comment inclusivity. Using default setting (N).")
        inclusive = "n"

    parent = input("Would you like to search parent comments? (Y/N) (Def:N): ")
    parent = parent.lower()
    if parent == "":
        print("No input for searching parent comments. Using default setting (N).")
        parent = "n"
    if parent == "no":
        parent = "n"
    if parent == "yes":
        parent = "y"
    if parent != "n" and parent != "y":
        print("Invalid input for searching parent comments. Using default setting (N).")
        parent = "n"

    web_open = input("Would you like to open the comment in a new tab? (Y/N) (Def:N): ")
    web_open = web_open.lower()
    if web_open == "":
        print("No input for opening comment in new tab. Using default setting (N).")
        web_open = "n"
    if web_open == "no":
        web_open = "n"
    if web_open == "yes":
        web_open = "y"
    if web_open != "n" and web_open != "y":
        print("Invalid input for opening comment in new tab. Using default setting (N).")
        web_open = "n"
    else:
        import webbrowser

    all_comments = input("Would you like to retrieve all comments? (Y/N) (Def:Y): ")
    all_comments = all_comments.lower()
    if all_comments == "":
        print("No input for retrieving all comments. Using default setting (Y).")
        all_comments = "y"
    if all_comments == "yes":
        all_comments = "y"
    if all_comments == "no":
        all_comments = "n"
    if all_comments != "n" and all_comments != "y":
        print("Invalid input for retrieving all comments. Using default setting (Y).")
        all_comments = "y"

    search = search.lower()
    search_list = set(search.split(","))
    terms = []
    for element in search_list:
        terms.append(element.strip())

    user = reddit.redditor(name)
    comment_list = user.comments.new(limit=1000)

    if inclusive != "y":
        for term in terms:
            term = term.strip()
            found = False
            print("\n###")
            print(f"Finding comments containing: \"{term}\"..")

            for comment in comment_list:
                comment_body = comment.body.replace("*", "").replace("_", "").replace("#", "")

                if term in comment_body.lower():
                    print(f"\n____\nFound comment!\nComment url: https://reddit.com/{comment.permalink}\n\n{comment.body}\n____\n")
                    if web_open == "y":
                        webbrowser.open(f"https://reddit.com/{comment.permalink}", new=0)
                    found = True
                    if all_comments != "y":
                        break

                if parent == "y":
                    parent_comment = comment.parent()

                    if "t1" not in parent_comment.fullname:
                        continue
                    parent_comment_body = parent_comment.body.replace("*", "").replace("_", "").replace("#", "")

                    if term in parent_comment_body.lower():
                        print(f"\n____\nFound in parent comment!\nComment url: https://reddit.com/{parent_comment.permalink}\n\n{parent_comment.body}\n____\n")
                        if web_open == "y":
                            webbrowser.open(f"https://reddit.com/{parent_comment.permalink}", new=0)
                        found = True
                        if all_comments != "y":
                            break

            if found == False:
                print(f"Couldn't find any comment containing: \"{term}\".")
            print("\n###\n")
    else:
        print("\n###")
        print(f"Finding comments containing: {terms}..")

        for comment in comment_list:
            comment_body = comment.body.replace("*", "").replace("_", "").replace("#", "")

            if all(term in comment_body.lower() for term in terms):
                print(f"\n____\nFound comment!\nComment url: https://reddit.com/{comment.permalink}\n\n{comment.body}\n____\n")
                if web_open == "y":
                    webbrowser.open(f"https://reddit.com/{comment.permalink}", new=0)
                found = True
                if all_comments != "y":
                    break

            if parent == "y":
                parent_comment = comment.parent()
                if "t1" not in parent_comment.fullname:
                    continue
                parent_comment_body = parent_comment.body.replace("*", "").replace("_", "").replace("#", "")

                if all(term in parent_comment_body.lower() for term in terms):
                    print(f"\n____\nFound in parent comment!\nComment url: https://reddit.com/{parent_comment.permalink}\n\n{parent_comment.body}\n____\n")
                    if web_open == "y":
                        webbrowser.open(f"https://reddit.com/{parent_comment.permalink}", new=0)
                    found = True
                    if all_comments != "y":
                        break

        if found == False:
            print(f"Couldn't find any comment containing: {terms}.")
        print("\n###\n")
