# inp_string = 'Hello'
# bytes_encoded = inp_string.encode()
# print(bytes_encoded)
import sqlite3
def add_data(data, emotion, type_media):
    if type_media == 'картинка':
        # with open(data, mode='rb') as file:
        #     file = file.read()
        file = data
    else:
        file = data.encode()
    # print(file)
    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()
    emotion_id = cur.execute('''SELECT id FROM Emotions WHERE emotion_name=?''', (emotion,)).fetchall()
    type_id = cur.execute('''SELECT id FROM Media WHERE media_type=?''', (type_media,)).fetchall()
    # print(file, emotion_id[0][0], type_id[0][0])
    sqlite_insert = """INSERT INTO Data (data, emotion_id, type_id) VALUES (?, ?, ?)"""
    # print(emotion_id[0][0], type_id[0][0])
    cur.execute(sqlite_insert, (file, emotion_id[0][0], type_id[0][0]))
    
    con.commit()
    cur.close()

def get_data(type_media, emotion_name):
    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()
    # emotion_id = cur.execute(f"""SELECT emotion_id from Emotions WHERE emotion_name={emotion_name}""")
    # media_id = cur.execute(f"""SELECT media_id from Media WHERE media_type={type_media}""")
    # result = cur.execute(f"""SELECT data from Data WHERE emotion_id={emotion_id} AND type_id={media_id} """).fetchall()
    result = cur.execute('''SELECT data FROM Data 
    WHERE emotion_id IN (SELECT id from Emotions WHERE emotion_name=?) AND 
    type_id IN (SELECT id from Media WHERE media_type=?)''', (emotion_name, type_media)).fetchall()
    answer = []
    for dat in result:
        answer.append(dat[0].decode() if type_media == 'музыка' else dat[0])
    return answer
    cur.close()
# add_data('картинка', 'радость', 'file.png')
# get_data('музыка', 'радость')
# add_data('https://music.youtube.com/watch?v=ncpQM2FxtmQ&list=RDAMVM8onXlXfbOXs', 'гнев', 'музыка')
# treks = get_data('музыка', 'гнев')
# print(treks)