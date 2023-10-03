import mysql.connector

# 信息
persons = [{'person_name':'a1','skills':'talk','summary':'kkkkkk','skill2':'math'},
           {'person_name':'a2','skills':'community','summary':'111111','skill2':'math'},
           {'person_name':'a3','skills':'dance','summary':'222222','skill2':'pe'},
           {'person_name':'a4','skills':'community','summary':'aaaaaa','skill2':'pe'}]


#连接数据库
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="238978",
    database="pythonsql"
)
#创建cursor
cursor = conn.cursor()

#输入人员信息
#query person，确定没有他的信息
for person in persons:  #因为人员是用字典表示的
    person_value = list(person.values()) #将字典转换成为列表
    print("person value is "+str(person_value)) #查看列表内容
    query_person = "select name, summary from person" #查询语句，查询
    cursor.execute(query_person) #执行查询语句，并传参
    outcome = cursor.fetchall() #查看sql语句返回结果
#再检查信息
    a1name = person_value[0] #姓名
    a1summary = person_value[2] #简介

    existedName = any(a1name == row[0] and a1summary == row[1] for row in outcome)
    #上面这一行还可以写成：
    #existedName = False
    #for row in outcome:
    #    if a1name == row[0] and a1summary == row[1]:
    #        existedName = True
#如果不存在
    if not existedName:
        name_insert = "insert into person (Name,summary) values (%s,%s)"
        cursor.execute(name_insert,(a1name,a1summary,))
        conn.commit()


#检查skill是否存在，先querytable取值
    query_skills = "select name from skills" #查询技能先
    cursor.execute(query_skills) #执行查询语句
    result = cursor.fetchall() #记录结果
    print(f"query skill table result is: "+str(result)) #查看结果
    existing_skills1 = [] #创建列表
    for row in result:
        existing_skills1.append(row[0]) #记录查询结果
    insert_query_skills = "insert into skills (Name) values (%s)" #插入语句
    existing_skills = set(existing_skills1) #将list转化成set
    skill_list = [] #创建列表记录准备需要输入的skill
    #获取skill1
    skill1 = person_value[1] #取第一个skill
    skill_list.append(skill1) #将第一个skill输入列表
    #获取skill2
    skill2 = person_value[3] #去第二个skill
    skill_list.append(skill2) #将第二个skill输入列表
    skill = set(skill_list) #将skill转换成set
    only_new = list(skill-existing_skills) #新技能set减去查询结果set，结果为多出来的set
    for i in only_new:
        cursor.execute(insert_query_skills,(i,)) #将结果输入数据库
        conn.commit()

#更新bridge table
#获取id
    query_to_get_id_person = (f"select id from person where name= %s")
    cursor.execute(query_to_get_id_person, (person_value[0],))
    person_id_from_person = cursor.fetchall()
    for person_id in person_id_from_person:
        person_id = person_id[0]
        print(person_id)
    print(f"person_id: {person_id_from_person}")

#通过id复查姓名
    query_to_get_name_person = (f"select name from person where id= %s")
    cursor.execute(query_to_get_name_person, (person_id,))
    person_name_from_person = cursor.fetchall()
    print(f"person_name: {person_name_from_person}")

#获取技能1id
    query_to_get_id_skill = f"select id from skills where name=%s"
    cursor.execute(query_to_get_id_skill,(person_value[1],))
    skill_id_from_person = cursor.fetchall()
    #print(f"skill1_id: {skill_id_from_person}")
    for i in skill_id_from_person:
        skill1_id = i[0]
        print(f"skill1 id is {skill1_id}")

#获取技能2id
    query_to_get_id_skill = f"select id from skills where name=%s"
    cursor.execute(query_to_get_id_skill,(person_value[3],))
    skill2_id_from_person = cursor.fetchall()
    #print(f"skill2_id: {skill2_id_from_person}")
    for i in skill2_id_from_person:
        skill2_id = i[0]
        print(f"skill2 id is {skill2_id}")

        # 构造数组，检查本表
        # skill1
        skill1_list = [person_id, skill1_id]
        # skill2
        skill2_list = [person_id, skill2_id]
        # 再查询bridge table
        query_bridge = "select person_id, skill_id from person_skills"
        cursor.execute(query_bridge)
        outcome = cursor.fetchall()

        # 插入语句
        insert_bridge_query = "insert into person_skills (person_id, skill_id) values (%s,%s)"
        cursor.execute(insert_bridge_query,(person_id,skill1_id))
        conn.commit()
        cursor.execute(insert_bridge_query,(person_id,skill2_id))
        conn.commit()
        """
        skill_fron_bridge = []
        for i in outcome:
            result_from_bridge = []
            result_from_bridge.append(i[0])
            result_from_bridge.append(i[1])
            print(f'rfb {result_from_bridge}')
            existedBridge = False
            for rbf in result_from_bridge:
                if rbf != skill1_list:
                    cursor.execute(insert_bridge_query, (person_id, skill1_id))
                    conn.commit()
                elif rbf != skill2_list:
                    cursor.execute(insert_bridge_query, (person_id, skill2_id))
                    conn.commit()
"""


"""
    query_to_get_id_person = (f"select id from person where name= %s")
    cursor.execute(query_to_get_id_person,(person_value[0],))
    person_id_from_person = cursor.fetchall()
    #建立list，记录答案
    bridgeList = []
    bridgeList.append(person_id_from_person)
    #在查询skill_id
    query_to_get_id_skill = f"select id from skills where name=%s"
    cursor.execute(query_to_get_id_skill,(person_value[1],))
    skill_id_from_person = cursor.fetchall()
    bridgeList.append(skill_id_from_person)
    #检查bridge list的值
    print("bridge list = "+str(bridgeList))

    #再查询bridge table
    query_bridge = "select person_id, skill_id from person_skills"
    cursor.execute(query_bridge)
    outcome = cursor.fetchall()
    existedBridge = False
    for row in outcome:
        if bridgeList[0][0][0] == row[0] and bridgeList[1][0][0] == row[1]:
            existedBridge = True


    if not existedBridge:
        insert_bridge_query = "insert into person_skills (person_id, skill_id) values (%s,%s)"
        cursor.execute(insert_bridge_query,(bridgeList[0][0][0],bridgeList[1][0][0]))


    conn.commit()
    """
conn.close()
