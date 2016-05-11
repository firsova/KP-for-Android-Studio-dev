import sqlite3
import os, os.path
import sys

class DisqusDB:

    '''
        Connects to database and creates tables if they don't exist
    '''
    def connect_to_db(self):
        try:
            s = os.path.dirname(os.path.abspath(__file__))
            conn = sqlite3.connect(s + "/disqus.db")
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS category (category_id integer NOT NULL, section_uuid text NOT NULL, \
                section_title text, UNIQUE(section_uuid) ON CONFLICT IGNORE)")
            c.execute("CREATE TABLE IF NOT EXISTS thread(thread_id integer NOT NULL, category_id integer NOT NULL, \
                identifier text NOT NULL, presentation_title text, speaker_name text, UNIQUE(thread_id, identifier) ON CONFLICT IGNORE)")
            c.execute("CREATE TABLE IF NOT EXISTS current(section_uuid text, timeslot_uuid text)")
            conn.commit()
            return conn
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            raise
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            raise
        except:
            sys.stderr.write("Unknown fatal error\n")
            raise

    '''
        Inserts category_id, section_uuid, section_title into database
    '''
    def add_category_to_db(self, cat_id, uuid, title):
        try:
            if not isinstance(uuid, unicode):
                uuid = uuid.decode('utf-8')
            if not isinstance(title, unicode):
                title = title.decode('utf-8')
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute("INSERT OR IGNORE INTO category VALUES (?, ?, ?)", [cat_id, uuid, title])
            conn.commit()
            conn.close()
            return "Success"
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            raise e
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            raise e
        except:
            sys.stderr.write("Unknown fatal error\n")
            raise

    '''
        Inserts thread_id, category_id, identifier, presentation_title, speaker_name into database
    '''
    def add_thread_to_db(self, thread_id, cat_id, ident, title, speaker):
        try:
            if not isinstance(ident, unicode):
                ident = ident.decode('utf-8')
            if not isinstance(title, unicode):
                title = title.decode('utf-8')
            if not isinstance(speaker, unicode):
                speaker = speaker.decode('utf-8')
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute("INSERT OR IGNORE INTO thread VALUES (?, ?, ?, ?, ?)", [thread_id, cat_id, ident, title, speaker])
            conn.commit()
            conn.close()
            return "Success"
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            raise e
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            raise e
        except:
            sys.stderr.write("Unknown fatal error\n")
            raise

    '''
        Retrieves category_id, section_uuid, section_title of all or one particular section from database
    '''
    def get_categories_from_db(self, cat_id = None):
        try:
            conn = self.connect_to_db()
            c = conn.cursor()
            rows = None
            if not cat_id:
                c.execute("SELECT * FROM category ORDER BY category_id ASC")
            else:
                c.execute("SELECT * FROM category WHERE category_id = ?", (cat_id, ))
            rows = c.fetchall()
            conn.commit()
            conn.close()
            return rows
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            raise e
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            raise e
        except:
            sys.stderr.write("Unknown fatal error\n")
            raise

    def get_category_from_db(self, section_uuid):
        try:
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute("SELECT category_id from category WHERE section_uuid = ?", (section_uuid, ))
            section = c.fetchone()
            if section:
                section = section[0]
            return section
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            raise e
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            raise e
        except:
            sys.stderr.write("Unknown fatal error\n")
            raise

    '''
    Retrieves identifier, presentation_title, speaker_name, section_title of all threads of a given section from database
    '''
    def get_threads_from_db(self, section_uuid):
        try:
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute('''SELECT category_id, section_title FROM category WHERE section_uuid = ?''', (section_uuid, ))
            category = None
            category = c.fetchone()
            if not category:
                return None
            category_id, section_title = category
            c.execute('''SELECT identifier, presentation_title, speaker_name 
                FROM thread WHERE category_id = ? ORDER BY thread_id ASC''', (category_id, ))
            rows = None
            rows = c.fetchall()
            if not rows:
                return None
            conn.commit()
            conn.close()
            return [rows, section_title]
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            raise e
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            raise e
        except:
            sys.stderr.write("Unknown fatal error\n")
            raise

    '''
        Retrieves thread_id, category_id, presentation_title, speaker_name, section_title of a thread with given identifier
    '''
    def get_thread_from_db(self, identifier):
        try:

            if not isinstance(identifier, unicode):
                identifier = identifier.decode("utf-8")

            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute('''SELECT thread_id, category_id, presentation_title, speaker_name 
                FROM thread WHERE identifier = ?''', (identifier, ))

            thread = None
            thread = c.fetchone()

            if thread is None:
                return None

            thread_id, category_id, title, speaker = thread
            c.execute('''SELECT section_title FROM category WHERE category_id = ?''', (category_id, ))

            section_title = ""
            section_title = c.fetchone()

            if section_title != "":
                section_title = section_title[0]
                section_title = section_title.encode("utf-8")
            conn.commit()
            conn.close()
            return [thread_id, category_id, title, speaker, section_title]
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            raise e
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            raise e
        except:
            sys.stderr.write("Unknown fatal error\n")
            raise

    '''
    Only for synchronizing with Disqus.com
    Deletes all rows from database
    '''
    def delete_all_from_tables(self):
        try:
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute("DELETE FROM category")
            c.execute("DELETE FROM thread")
            conn.commit()
            conn.close()
            return "Success"
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            raise
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            raise
        except:
            sys.stderr.write("Unknown fatal error\n")
            raise

    '''
        Sets section_uuid of the current section in database
    '''
    def set_current_section(self, section_uuid):
        try:
            if not isinstance(section_uuid, unicode):
                section_uuid = section_uuid.decode("utf-8")
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute("SELECT count(*) FROM current")
            s = ""
            if c.fetchone()[0] > 0:
                c.execute("UPDATE current SET section_uuid = ?", (section_uuid, ))
                s = "Updated table 'current': set new section_uuid={}\n".format(section_uuid)
            else:
                c.execute("INSERT INTO current(section_uuid, timeslot_uuid) VALUES (?, NULL)", (section_uuid, ))
                s = "Inserted into table 'current' new section_uuid={}\n".format(section_uuid)
            conn.commit()
            conn.close()
            return "Success. " + s
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            return "sqlite3 error: {}".format(str(e))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            return "Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e))
        except:
            sys.stderr.write("Unknown fatal error\n")
            return "Unknown fatal error\n"

    '''
        Sets timeslot_uuid of the current presentation in database
    '''
    def set_current_presentation(self, timeslot_uuid):
        try:
            if not isinstance(timeslot_uuid, unicode):
                timeslot_uuid = timeslot_uuid.decode("utf-8")
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute("SELECT count(*) FROM current")
            s = ""
            if c.fetchone()[0] > 0:
                c.execute("UPDATE current SET timeslot_uuid = ?", (timeslot_uuid, ))
                s = "Updated table current: set new timeslot_uuid={}\n".format(timeslot_uuid)
            else:
                c.execute("INSERT INTO current(section_uuid, timeslot_uuid) VALUES (NULL, ?)", (timeslot_uuid, ))
                s = "Inserted into table current new timeslot_uuid={}\n".format(timeslot_uuid)
            conn.commit()
            conn.close()
            return "Success. " + s
        except sqlite3.Error as e:
            sys.stderr.write("sqlite3 error: {}".format(str(e)))
            return "sqlite3 error: {}".format(str(e))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            return "Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e))
        except:
            sys.stderr.write("Unknown fatal error\n")
            return "Unknown fatal error\n"

    '''
        Clears the table with the current section in database
    '''
    def end_current_section(self):
        try:
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute("UPDATE current SET section_uuid = NULL, timeslot_uuid = NULL")
            c.execute("DELETE FROM current")
            c.execute("INSERT INTO current(section_uuid, timeslot_uuid) VALUES (NULL, NULL)")
            conn.commit()
            conn.close()
            return "Success"
        except sqlite3.Error as e:
            sys.stderr.write("sqlite3 error: {}".format(str(e)))
            return "sqlite3 error: {}".format(str(e))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            return "Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e))
        except:
            sys.stderr.write("Unknown fatal error\n")
            return "Unknown fatal error\n"

    '''
        Sets timeslot_uuid in the table of the current section to NULL
    '''
    def end_current_presentation(self):
        try:
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute("SELECT timeslot_uuid FROM current")
            timeslot_uuid = c.fetchone()
            if timeslot_uuid:
                timeslot_uuid = timeslot_uuid[0]
                c.execute("UPDATE current SET timeslot_uuid = NULL WHERE timeslot_uuid = ?", (timeslot_uuid, ))
            conn.commit()
            conn.close()
            return "Success"
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            return "Error"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            return "Error"
        except:
            sys.stderr.write("Unknown fatal error\n")
            return "Error"

    '''
        Retrieves section_uuid and timeslot_uuid of the current section and presentation
    '''
    def get_current_event(self):
        try:
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute("SELECT * FROM current")
            event = c.fetchone()
            conn.commit()
            conn.close()
            return event
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            raise
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            raise
        except:
            sys.stderr.write("Unknown fatal error\n")
            raise

    def get_rows_count(self):
        try:
            conn = self.connect_to_db()
            c = conn.cursor()
            c.execute("SELECT count(*) FROM category")
            count = c.fetchone()[0]
            conn.commit()
            conn.close()
            return count
        except sqlite3.Error as e:
            sys.stderr.write ("sqlite3 error: {}".format(str(e)))
            raise
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            sys.stderr.write ("Error in {} on line {}: {}".format(fname, exc_tb.tb_lineno, str(e)))
            raise
        except:
            sys.stderr.write("Unknown fatal error\n")
            raise
