import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
import os

db_url = os.environ["SQLALCHEMY_DATABASE_URI"]
db_url = "postgresql:" + db_url.split(":", 1)[1]
print(db_url)
engine = create_engine(db_url)

user_queries = [
    """ CREATE TABLE public."user" (
    id integer NOT NULL,
    name text,
    email character varying(100) NOT NULL,
    hashed_password text NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    is_superuser boolean DEFAULT false NOT NULL,
    last_name text
);""",
    """ALTER TABLE public."user" OWNER TO furkana;
CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 """,
    """ALTER TABLE public.user_id_seq OWNER TO furkana;""",
    """ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;""",
    """ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);""",
    """ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);""",
    """ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);""",
    """CREATE INDEX idx_user_email_1b4f1c ON public."user" USING btree (email);""",
]

log_queries = [
    """CREATE TABLE public.log (
    id integer NOT NULL,
    query_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    picture_path text NOT NULL,
    result text NOT NULL,
    user_id integer NOT NULL
); """,
    """ALTER TABLE public.log OWNER TO furkana;""",
    """CREATE SEQUENCE public.log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;""",
    """ALTER TABLE public.log_id_seq OWNER TO furkana;""",
    """ALTER SEQUENCE public.log_id_seq OWNED BY public.log.id;""",
    """ALTER TABLE ONLY public.log ALTER COLUMN id SET DEFAULT nextval('public.log_id_seq'::regclass);""",
    """ALTER TABLE ONLY public.log
    ADD CONSTRAINT log_pkey PRIMARY KEY (id);""",
    """ALTER TABLE ONLY public.log
    ADD CONSTRAINT log_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;""",
]
from sqlalchemy.sql import text

if __name__ == "__main__":
    with engine.connect() as con:
        try:
            print("Checking if user table exists")
            res = con.execute("""SELECT * FROM public.user""")
            print("Table already exists.")
        except sqlalchemy.exc.ProgrammingError as e:
            if e.args[0].split(" ")[0] == "(psycopg2.errors.UndefinedTable)":
                print("Table doesn't exists. Creating.")
                for queries in user_queries:
                    con.execute(queries)
                print("user table Created.")

        try:
            print("Checking if log table exists")
            res = con.execute("""SELECT * FROM public.log""")
            print("Table already exists.")
        except sqlalchemy.exc.ProgrammingError as e:
            if e.args[0].split(" ")[0] == "(psycopg2.errors.UndefinedTable)":
                print("Table doesn't exists. Creating.")
                for queries in log_queries:
                    con.execute(queries)
                print("log table Created.")
