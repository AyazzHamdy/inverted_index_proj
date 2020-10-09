
import functions as funcs
import re
import os



def csv_to_df(cur_dir):

    original_file_path = os.path.join(cur_dir, 'sms.csv')
    remedy_file_path = os.path.join(cur_dir, 'sms_remedy.csv')
    remedy_file = funcs.WriteFile(cur_dir, "sms_remedy", "csv", f_mode="w+")
    print(" Step 1/A: Fixing input CSV issues; extra quotes/missing quotes  \n ")
    with open(original_file_path, encoding="utf8") as reading_file:
        lines_list = reading_file.readlines()

        for i in range(len(lines_list)):
            try:
                next_line_peek = lines_list[i+1]
                end_of_msg_block_flag = True if next_line_peek.find(',"') != -1 else False
                regex_emoji = re.compile(r'\d\d\d\d\d\d,[\u263a-\U0001f645]')
                regex_missing_quotes = re.compile(r'\d\d\d\d\d\d,\w')
                if len(regex_missing_quotes.findall(next_line_peek)) != 0 or len(regex_emoji.findall(next_line_peek)) != 0:
                    end_of_msg_block_flag = True
                    erroneous_msg_i = i + 1

            except:
                end_of_msg_block_flag = True

            new_line = lines_list[i]
            new_line = new_line.replace('""', '"')
            try:
                if erroneous_msg_i == i:
                    line_split = new_line.split(',', 1)
                    re_form_line_q = line_split[0] + ',"'
                    re_form_line_q = re_form_line_q + line_split[1].strip() + '"'+"\n"
                    new_line = re_form_line_q
                    remedy_file.write(new_line)
                    continue
            except:
                pass

            if new_line.find(',"') != -1:
                line_split = new_line.split(',"')
                re_form_line = line_split[0] + ',"'

                for j in range(len(line_split)):
                    if j == 0: continue
                    if end_of_msg_block_flag is False:

                        re_form_line += line_split[j].replace('"',' ')
                    else:
                        quotes_count = line_split[j].count('"')
                        if quotes_count == 1:
                            re_form_line += line_split[j]
                        else:
                            re_form_line += line_split[j].replace('"', ' ', quotes_count-1)

                new_line = re_form_line

            elif end_of_msg_block_flag is True:
                quotes_count = new_line.count('"')
                if quotes_count == 1:
                    new_line = new_line
                else:
                    new_line = new_line.replace('"', ' ', quotes_count-1)
            elif not end_of_msg_block_flag:
                new_line = new_line.replace('"', ' ')

            remedy_file.write(new_line)
    remedy_file.close()
    print(" Step 1/A Completed csv remedy_file generated  \n ")
    print(" Step 1/B Constructing DF from the remedied CSV file  \n ")
    sms_df = funcs.read_csv(remedy_file_path)
    print(" Step 1/B Completed  \n ")

    return sms_df


def df_to_dict(sms_df):

    Dict = {}
    for sms_df_index, sms_df_row in sms_df.iterrows():
        msg_id = sms_df_row['id']
        msg = sms_df_row['message']

        msg_split = re.split("\s|,|\n", msg)

        for j in range(len(msg_split)):
            word = msg_split[j]

            if word.isnumeric():
                continue
            word = funcs.replace_chars(word)
            word_pos = msg_id
            if word not in funcs.get_stop_words() and word.isalnum():
                if Dict.get(word):
                    word_pos_list = Dict.get(word)
                    word_pos_list.append(word_pos)
                else:
                    word_pos_list = [word_pos]
                Dict[word] = word_pos_list

    return Dict


def retrieve_messages(search_key, dict, msg_df, cur_dir):
    count_msg_matches = 0
    try:
        relevant_msg_ids = dict.get(search_key)
        relevant_msg_df = msg_df[msg_df['id'].isin(relevant_msg_ids)]
        search_result_file = funcs.WriteFile(cur_dir, "search_result", "txt", f_mode="w+")

        count_msg_matches = len(relevant_msg_ids)

        search_result_file.write("The following are the messages containing search_word: (', search_key,'):"+'\n')

        for relevant_msg_df_index, relevant_msg_df_row in relevant_msg_df.iterrows():
            message_id = relevant_msg_df_row['id']
            message_txt = relevant_msg_df_row['message']

            search_result_file.write("message_id:{}\nmessage_text:{}\n".format(message_id , message_txt))
            # print("message_id:{}\nmessage_text:{}\n".format(message_id, message_txt))
    except:
        count_msg_matches = 0
        search_result_file.write("word not found")
        # print("word not found")

    return count_msg_matches
if __name__ == '__main__':

    cur_dir = os.getcwd()
    print(" Step 1: Starting Reading CSV into DataFrame \n ")
    sms_df = csv_to_df(cur_dir)
    print(" Reading CSV into DataFrame Completed \n ")
    print(" Step 2: Starting Building Dictionary \n")
    dict= df_to_dict(sms_df)
    print(" Building Dictionary Completed ")
    print(" Step 3: Retrieving Messages containing your search word \n")
    search_res = retrieve_messages('تحت', dict, sms_df, cur_dir)
    if search_res == 0:
        print("word not found")
    else:
        print(" Search Completed \n You Can Check search_result.txt ")

