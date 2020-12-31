import pandas as pd

def FindAllCharacters():
    diffrent_characters = []
    file_address = 'data/{}.csv'
    for file_number in range(1,7):
        print(file_number, "new FILE! ===================")
        df = pd.read_csv(file_address.format(file_number))
        news_count = df.shape[0]
        for news_id in range(news_count):
            if news_id % 200 == 0:
                print(news_id, " %%%%%%%%%%%%%%%%%%%%%%")
            main_content = df.loc[news_id, 'content']
            for single_character in main_content:
                if single_character not in diffrent_characters:
                    diffrent_characters.append(single_character)


    with open("news_characters.txt","a") as target_file:
        for character in diffrent_characters:
            target_file.write(character+'\n')

FindAllCharacters()
