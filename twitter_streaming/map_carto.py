import folium 
import mysql.connector 

conn = mysql.connector.connect(user = 'root', host = 'localhost', database = 'db_twitter', charset = 'utf8mb4')
curseur = conn.cursor()

sql = 'SELECT `place`,`latitude`,`longitude`,`user_name` FROM tweets_streaming'


curseur.execute(sql)
myresult = curseur.fetchall()

m = folium.Map(location = [45,5], tiles = "OpenStreetMap", zoom_start = 5)

# sql = 'SELECT `place`, `lat_1`, `long_1`, `lat_2`, `long_2`, `lat_3`, `long_3`, `lat_4`, `long_4`, `lat_5`, `long_5` FROM tweet_place'


# curseur.execute(sql)
# liste_places = curseur.fetchall()


# #mise en forme de la ligne brisée pour les polygones
# def transform_coord(place):
	
# 	point1 = (float(place[1]),float(place[2]))
# 	point2 = (float(place[3]),float(place[4]))
# 	point3 = (float(place[5]),float(place[6]))
# 	point4 = (float(place[7]),float(place[8]))
# 	point5 = (float(place[9]),float(place[10]))
		
# 	return [point1, point2, point3, point4, point5]




# #tracer les polygones représentants les cities
# print(liste_places)
# for place in liste_places:
# 	print(transform_coord(place))

# 	folium.PolyLine(transform_coord(place), color = 'darkred', weight = 2.5, opacity = '0.7').add_to(m)



#ping les places de la table tweet_geo
for geoloc in range(len(myresult)):
	folium.Marker(
		location = [myresult[geoloc][1],myresult[geoloc][2]],
		icon =folium.Icon(color =  'blue', icon = 'logo-twitter'),
		popup = myresult[geoloc][0]
		 ).add_to(m)
	

m.save("map.html")