from database.DB_connect import DBConnect
from model.actor import Actor


class DAO():

    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        results = []

        query = """
            select distinct r.avg_rating 
            from ratings r 
            order by r.avg_rating
        """

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllActors():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        results = []

        query = """
                select *
                from names n 
                where n.date_of_birth is not null
        """

        cursor.execute(query)

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllActorsByRatings(vMin, vMax):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        results = []

        query = """
                select distinct n.*
                from names n, role_mapping rm, movie m, ratings r
                where n.id = rm.name_id and rm.movie_id = m.id and r.movie_id = m.id 
                and r.avg_rating >= %s and r.avg_rating <= %s and n.date_of_birth is not null
        """

        cursor.execute(query, (vMin, vMax))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(vMin, vMax):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        results = []

        query = """
                select t1.name_id as act1, t2.name_id as act2, t1.worlwide_gross_income as income
                from 
                (
                    select rm.name_id, m.id, m.worlwide_gross_income 
                    from names n, role_mapping rm, movie m, ratings r
                    where n.id = rm.name_id and rm.movie_id = m.id and r.movie_id = m.id 
                    and r.avg_rating >= %s and r.avg_rating <= %s and n.date_of_birth is not null 
                    and m.worlwide_gross_income is not null
                ) as t1,
                (
                    select rm.name_id, m.id, m.worlwide_gross_income 
                    from names n, role_mapping rm, movie m, ratings r
                    where n.id = rm.name_id and rm.movie_id = m.id and r.movie_id = m.id 
                    and r.avg_rating >= %s and r.avg_rating <= %s and n.date_of_birth is not null 
                    and m.worlwide_gross_income is not null
                ) as t2
                where t1.name_id < t2.name_id and t1.id = t2.id
        """

        cursor.execute(query, (vMin, vMax, vMin, vMax))

        for row in cursor:
            results.append((row["act1"], row["act2"], row["income"]))

        cursor.close()
        conn.close()
        return results