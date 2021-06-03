import folium 
import mysql.connector 
from nominatim import Nominatim
from tokenization import list_word_most_common
from check_tweets_in_cities import get_tweets_in_city

conn = mysql.connector.connect(user = 'root', host = 'localhost', database = 'db_twitter', charset = 'utf8mb4')
curseur = conn.cursor()

sql = 'SELECT DISTINCT `place` FROM tweets_streaming'


curseur.execute(sql)
myresult = curseur.fetchall()



m = folium.Map(location = [45,5], tiles = "OpenStreetMap", zoom_start = 5)

sql = 'SELECT `place`, `lat_1`, `long_1`, `lat_2`, `long_2`, `lat_3`, `long_3`, `lat_4`, `long_4` FROM polygon'


curseur.execute(sql)
liste_places = curseur.fetchall()

#mise en forme de la ligne brisée pour les polygones
def transform_coord(place):
	
	point1 = (float(place[1]),float(place[2]))
	point2 = (float(place[3]),float(place[4]))
	point3 = (float(place[5]),float(place[6]))
	point4 = (float(place[7]),float(place[8]))
	point5 = (float(place[1]),float(place[2]))
		
	return [point1, point2, point3, point4, point5]
	
#tracer les polygones représentants les cities

for place in liste_places:

	# print(transform_coord(place))

	folium.PolyLine(
		transform_coord(place),
		color = 'darkred', 
		weight = 2.5, 
		opacity = '0.7').add_to(m)




import re
nom = Nominatim()

def get_city_center(city):
	
	
	for c in city:
		
		if c == "é" or c == "è" or c == "ê" or c == "ë":
			city = city.replace(c,"e")
		if c == "à" or c == "â" or c == "ä":
			city = city.replace(c,"a")
		if c == "û" or c == "ù" or c == "ü":
			city = city.replace(c,"u")	
		if c == "î" or c == "ï":
			city = city.replace(c,"i")	
		if c == "ô" or c == "ö":
			city = city.replace(c,"o")
		if c == "ç":
			city = city.replace(c,"c")	
			
	
	place = nom.query(city)[0]


	return [place["lat"], place["lon"]]


for geoloc in myresult:
	# print(geoloc[0])
	# get_tweets_in_city(geoloc[0])
	list_word_most_common(geoloc[0])

#ping les places de la table tweet_geo
for geoloc in myresult:
	folium.Marker(
		location = get_city_center(geoloc[0]),
		icon =folium.Icon(color =  'blue', icon = 'glyphicon glyphicon-circle-arrow-down'),
		popup = list_word_most_common(geoloc[0])
		 ).add_to(m)
	

m.save("map.html")

