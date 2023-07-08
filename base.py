import sqlite3

class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_queue(self, chat_id, user_name):
        with self.connection:
            return self.cursor.execute('insert into queue (chat_id, user_name) values (?,?)',(chat_id, user_name,))

    def delete_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute('delete from queue where chat_id = ?;', (chat_id,))

    def delete_chat(self, id_chat):
        return self.cursor.execute('delete from chats where id = ?;', (id_chat,))

    def get_chat(self):
        with self.connection:
            chat = self.cursor.execute('select * from queue').fetchmany(1)
            if(bool(len(chat))):
                for i in chat:
                    return i[1]
            else:
                return False

    def create_chat(self, chat_one, chat_two):
        with self.connection:
            if chat_two != 0:
                #Создание чата
                self.cursor.execute('delete from queue where chat_id = ?;', (chat_two,))
                self.cursor.execute('insert into chats (chat_one, chat_two) values (?,?)',(chat_one, chat_two,))
                return True
            else:
                #Становимся в очередь
                return False

    def get_active_chat(self, chat_id):
        chat = self.cursor.execute('select * from chats where chat_one = ?', (chat_id,))
        id_chat = 0
        for i in chat:
            id_chat = i[0]
            chat_info = [i[0], i[2]]

        if id_chat == 0:
            chat = self.cursor.execute('select * from chats where chat_two = ?', (chat_id,))
            for i in chat:
                id_chat = i[0]
                chat_info = [i[0], i[1]]
            if id_chat == 0:
                return False
            else:
                return chat_info
        else:
            return chat_info


    def watch_chat(self):
        check = self.cursor.execute('select * from chats').fetchall()
        if check == []:
            return False
        else:
            return True