
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort



class User:
    def UserLogin(self,UserName,pwd):
        cnxn = self
        cursor = cnxn.cursor()
        cursor.execute("select * from users where userName = %s and passwd =%s",(UserName,pwd))
        Users = cursor.fetchone()
        cursor.close()
        print(Users[0])
        return  Users

    def GetUser(self,id):
        cnxn = self
        cursor = cnxn.cursor()
        cursor.execute("select * from users where userId ="+str(id))
        Users = cursor.fetchone()
        cursor.close()
        print(Users[0])
        return  Users
    def GetUserByNmae(self,name):
        cnxn = self
        cursor = cnxn.cursor()
        cursor.execute("select * from users where userName =' "+name+"';")
        Users = cursor.fetchone()
        cursor.close()

        return  Users


class Food:
    def getData(self):
        cnxn = self
        cursor = cnxn.cursor()
        cursor.execute("select * from food_table limit 10")
        rows = cursor.fetchall()

        for row in rows:
            print(row)
        cnxn.close()
        return rows

    def getDetectFood(self, foodName):
        cnxn = self
        cursor = cnxn.cursor()

        command = ("select title from food_table where title like '%"+foodName+"%' limit 1;")

        cursor.execute(command)

        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()

        return rows



    def save_image(self, picUrl, foodname):

        cnxn = self
        cursor = cnxn.cursor()
        command = "INSERT into Food_image(FoodName,picUrl) VALUES (%s, %s);"
        val = (foodname, picUrl)
        cursor.execute(command, val)
        cnxn.commit()
        cursor.close()
        print(cursor.rowcount, "record inserted.")

class Record:
    def storeData(self,userId,foodId,times):
        cnxn = self
        cursor = cnxn.cursor()

        cursor.execute(('insert into Food_record (userId,FoodId,times) values (%s,%s,%s);'), (userId, foodId, times))
        cnxn.commit()
        cursor.close()
        return