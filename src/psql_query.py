import psycopg2
import pandas as pd
from config import init_connection
import streamlit as st

print('Connecting to the PostgreSQL database...')
pool = init_connection()

MIN_NUM_OF_OFFERS = 3


def basic_query(query: str) -> pd.DataFrame:
    df = pd.DataFrame
    conn = None
    cur = None
    try:
        print("Getting connection from the pool...")
        conn = pool.getconn()
        cur = conn.cursor()
        cur.execute(query)
        fetched_data = cur.fetchall()
        df = pd.DataFrame(fetched_data)
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    except Exception as error:
        print(error)
    finally:
        if cur is not None and not cur.closed:
            cur.close()
        if conn is not None:
            pool.putconn(conn)
            print('Putting connection to the pull')
    return df


def wrap_list_to_str(l: list) -> str:
    s = ' '.join(l)
    s = ', '.join("'{}'".format(word) for word in l)
    s = '(' + s + ')'
    return s


def get_query_with_params(loc: list = None, tech: list = None, exp: list = None, cat: list = None) -> pd.DataFrame:
    EXP_LVL_LIST = ['Trainee', 'Junior', 'Mid', 'Senior', 'Expert']
    cat_xor_tech = "technology" if tech else "category"
    if tech == [] and cat == []:
        cat_xor_tech_tuple = tuple(get_cat_list())
    else:
        cat_xor_tech_tuple = wrap_list_to_str(tech) if tech != [] else wrap_list_to_str(cat)
    loc_tuple = tuple(get_loc_list()) if loc == [] else wrap_list_to_str(loc)
    exp_tuple = tuple(EXP_LVL_LIST) if exp == [] else wrap_list_to_str(exp)
    all_loc = tuple(get_loc_list())
    all_cat_xor_tech = tuple(get_tech_list()) if tech != [] else tuple(get_cat_list())
    all_exp = tuple(EXP_LVL_LIST)

    return basic_query(f"""
                with no_copies AS (select id,
                                      city,""" + cat_xor_tech + f""",
                                      experience_level,
                                      (min(salary_from) + max(salary_from) + min(salary_to) + max(salary_to)) / 4 as salary
                               from job_offer
                                        left join job_category jc on job_offer.id = jc.offer_id
                                        left join job_employment_type jet on job_offer.id = jet.offer_id
                                        left join job_location jl on job_offer.id = jl.offer_id
                                        left join job_experience_level jel on job_offer.id = jel.offer_id
                               where city in {loc_tuple}
                                 and """ + cat_xor_tech + f""" in """ + f"""{cat_xor_tech_tuple}""" + f"""
                                 and experience_level in {exp_tuple}
                                 and salary_to IS NOT NULL
                               group by id, city, """ + cat_xor_tech + f""", experience_level
                               order by id)
            select max(city),
                   max(""" + cat_xor_tech + f"""),
                   max(experience_level),
                   CAST(ROUND(AVG(salary)) AS bigint) as  average,
                   CAST(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS bigint) AS median,
                   count(salary) as dem
            from no_copies
            group by (case when {len(all_loc)} != {len(loc_tuple)} then city end),
                     (case when {len(all_cat_xor_tech)} != {len(cat_xor_tech_tuple)} then """ + cat_xor_tech + f""" end),
                     (case when {len(all_exp)} != {len(exp_tuple)} then experience_level end);""")


@st.experimental_memo(ttl=600)
def get_offer_cnt():
    return basic_query(COUNT_OFFERS)[0][0]


@st.experimental_memo(ttl=600)
def get_avg_salary():
    return basic_query(AVG_SALARY)[0][0]


@st.experimental_memo(ttl=600)
def get_med_salary():
    return basic_query(MED_SALARY)[0][0]


@st.experimental_memo(ttl=600)
def get_loc_list():
    return basic_query(ALL_LOC)[0].tolist()


@st.experimental_memo(ttl=600)
def get_cat_list():
    return basic_query(ALL_CAT)[0].tolist()


@st.experimental_memo(ttl=600)
def get_tech_list():
    return basic_query(ALL_TECH)[0].tolist()


@st.experimental_memo(ttl=600)
def top_med_by_loc(top: float) -> pd.DataFrame:
    percent = top / 100
    return basic_query(f"""
            WITH salaries(loc, salary) AS (SELECT jl.city,
                                                  (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                           FROM job_employment_type jet
                                                    FULL JOIN job_location jl ON jet.offer_id = jl.offer_id
                                           WHERE salary_currency = 'PLN')
            SELECT loc, PERCENTILE_CONT({percent}) WITHIN GROUP (ORDER BY salary) AS median
            FROM salaries
            GROUP BY loc
            HAVING count(loc) > {MIN_NUM_OF_OFFERS}
            ORDER BY median DESC;""")


@st.experimental_memo(ttl=600)
def top_med_by_exp(top: float) -> pd.DataFrame:
    percent = top / 100
    return basic_query(f"""
            WITH salaries(exp, salary) AS (SELECT jel.experience_level,
                                                  (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                           FROM job_employment_type jet
                                                    FULL JOIN job_experience_level jel ON jet.offer_id = jel.offer_id
                                           WHERE salary_currency = 'PLN')
            SELECT exp, PERCENTILE_CONT({percent}) WITHIN GROUP (ORDER BY salary) as median
            FROM salaries
            GROUP BY exp
            HAVING count(exp) > {MIN_NUM_OF_OFFERS}
            ORDER BY median desc;""")


COUNT_BY_CAT = f"""
            SELECT category, count(*)
            FROM job_category
            WHERE category IS NOT NULL
            GROUP BY category
            HAVING count(category) > {MIN_NUM_OF_OFFERS}
            ORDER BY count(*) DESC;"""

COUNT_BY_TECH = f"""
            SELECT technology, count(*)
            FROM job_category
            WHERE technology IS NOT NULL
            GROUP BY technology
            HAVING count(technology) > {MIN_NUM_OF_OFFERS}
            ORDER BY count(*) DESC;"""

COUNT_BY_LOC = f"""
            SELECT city, count(*)
            FROM job_location
            WHERE city IS NOT NULL
            GROUP BY city
            HAVING count(*) > 5
            ORDER BY count(*) DESC;"""

COUNT_BY_EXP = f"""
            SELECT experience_level, count(*)
            FROM job_experience_level
            WHERE experience_level IS NOT NULL
            GROUP BY experience_level
            HAVING count(experience_level) > {MIN_NUM_OF_OFFERS}
            ORDER BY count(*) DESC;"""

AVG_BY_LOC = f"""
            SELECT jl.city, (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
            FROM job_employment_type jet
            FULL JOIN job_location jl ON jet.offer_id = jl.offer_id
            GROUP BY jl.city, jet.salary_currency
            HAVING count(salary_to) > {MIN_NUM_OF_OFFERS} AND jet.salary_currency = 'PLN' AND jl.city IS NOT NULL
            ORDER BY (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2 DESC;"""

AVG_BY_EXP = f"""
            SELECT jel.experience_level, (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
            FROM job_employment_type jet
            FULL JOIN job_experience_level jel ON jet.offer_id = jel.offer_id
            WHERE salary_currency = 'PLN'
            GROUP BY jel.experience_level, jet.salary_currency
            HAVING count(salary_to) > {MIN_NUM_OF_OFFERS}
            ORDER BY (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2 DESC;"""

AVG_BY_TECH = f"""
            SELECT jc.technology, (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
            FROM job_employment_type jet
            FULL JOIN job_category jc on jet.offer_id = jc.offer_id
            WHERE salary_currency = 'PLN'
            GROUP BY jc.technology, jet.salary_currency
            HAVING count(technology) > {MIN_NUM_OF_OFFERS}
            ORDER BY (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2 DESC;"""

AVG_BY_CAT = f"""
            SELECT jc.category, (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
            FROM job_employment_type jet
            FULL JOIN job_category jc on jet.offer_id = jc.offer_id
            WHERE salary_currency = 'PLN'
            GROUP BY jc.category, jet.salary_currency
            HAVING count(category) > {MIN_NUM_OF_OFFERS}
            ORDER BY (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2 DESC;"""

MED_BY_TECH = f"""
            WITH salaries(tech, salary) AS (SELECT jc.technology, (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                            FROM job_employment_type jet
                                            FULL JOIN job_category jc ON jet.offer_id = jc.offer_id
                                            WHERE salary_currency = 'PLN')
            SELECT tech, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median
            FROM salaries
            GROUP BY tech
            HAVING count(tech) > {MIN_NUM_OF_OFFERS}
            ORDER BY median DESC;"""

MED_BY_CAT = f"""
            WITH salaries(cat, salary) AS (SELECT jc.category, (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                            FROM job_employment_type jet
                                            FULL JOIN job_category jc ON jet.offer_id = jc.offer_id
                                            WHERE salary_currency = 'PLN')
            SELECT cat, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median
            FROM salaries
            GROUP BY cat
            HAVING count(cat) > {MIN_NUM_OF_OFFERS}
            ORDER BY median DESC;"""

MED_BY_LOC = f"""
            WITH salaries(loc, salary) AS (SELECT jl.city,
                                                  (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                           FROM job_employment_type jet
                                                    FULL JOIN job_location jl ON jet.offer_id = jl.offer_id
                                           WHERE salary_currency = 'PLN')
            SELECT loc, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median
            FROM salaries
            GROUP BY loc
            HAVING count(loc) > {MIN_NUM_OF_OFFERS}
            ORDER BY median DESC;"""

MED_BY_EXP = f"""
            WITH salaries(exp, salary) AS (SELECT jel.experience_level,
                                                  (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                           FROM job_employment_type jet
                                                    FULL JOIN job_experience_level jel ON jet.offer_id = jel.offer_id
                                           WHERE salary_currency = 'PLN')
            SELECT exp, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median
            FROM salaries
            GROUP BY exp
            HAVING count(exp) > {MIN_NUM_OF_OFFERS}
            ORDER BY median desc;"""

COUNT_OFFERS = f"""SELECT count(*) FROM job_offer;"""

AVG_SALARY = f"""
            SELECT (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
            FROM job_employment_type jet
            WHERE salary_currency = 'PLN';
            """

MED_SALARY = f"""
            WITH salaries(salary) AS (SELECT (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                      FROM job_employment_type jet
                                      WHERE salary_currency = 'PLN')
            SELECT CAST(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS bigint) AS median
            FROM salaries;"""

ALL_LOC = f"""
            SELECT city
            FROM job_location
            GROUP BY city
            HAVING count(city) > {MIN_NUM_OF_OFFERS}
            ORDER BY city;"""

ALL_CAT = f"""
            SELECT category
            FROM job_category
            GROUP BY category
            HAVING count(category) > {MIN_NUM_OF_OFFERS}
            ORDER BY category;"""

ALL_TECH = f"""
            SELECT technology
            FROM job_category
            GROUP BY technology
            HAVING count(technology) > {MIN_NUM_OF_OFFERS}
            ORDER BY technology;"""
