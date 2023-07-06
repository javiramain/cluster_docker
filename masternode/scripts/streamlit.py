from json import dumps

from kafka import KafkaProducer
from kafka import KafkaConsumer
# from pykafka.common import OffsetType
#pip install kafka-python


import streamlit as st
# from pykafka import KafkaClient

# client = KafkaClient(hosts='localhost:9095')
# inputTopic = client.topics[b'streaming-query']
# outputTopic = client.topics[b'output']
# inputProducer = inputTopic.get_sync_producer()
# outputConsumer = outputTopic.get_simple_consumer(auto_offset_reset=OffsetType.LATEST,
#     reset_offset_on_start=True)
# consumer = outputTopic.
# import requests
# from streamlit_lottie import st_lottie
# from PIL import Image
# from collections import Counter
#from confluent_kafka import Producer

st.title('Bienvenido a ElMercado.com')
st.header('Estás en la seccion de busqueda')
st.subheader('Busca aqui el artículo que quieras comprar')
articulo= st.text_input("Describe tu articulo")
# tienda = st.text_input("Quieres comprar en una tienda en particular? Introduce el nombre de la tienda")
buy = st.button('BUSCAR', 'key1', 'this button is used to buy stuff')
# initializing the Kafka producer
my_producer = KafkaProducer(
    bootstrap_servers = ['workernode1:9092'],
    value_serializer = lambda x:dumps(x).encode('utf-8')
    )
my_producer.send('streaming-query', value = articulo)
# if (articulo):
	# if(tienda):
	# 	#send_message(mensaje)
	# 	st.text(f"Quieres comprar un {articulo} en {tienda}")
	# 	st.caption("Aqui tienes las posibilidades. Haz click sobre una para acceder a la seccion de compra")
	# else:
	# 	st.text(f"Quieres comprar un {articulo} en cualquier tienda")
	# 	st.caption("Aqui tienes las posibilidades. Haz click sobre una para acceder a la seccion de compra")

# mensaje = articulo.encode(encoding='UTF-8')
# inputProducer.produce(mensaje)
# consumer = outputConsumer.get_simple_consumer(
#     auto_offset_reset=OffsetType.LATEST,
#     reset_offset_on_start=True)
# st.text(outputConsumer)
#def send_message(message):
#    p = Producer({'bootstrap.servers': 'localhost:9092'})
#    topic = 'mi-topico'  # Reemplaza con el nombre de tu tópico
#    p.produce(topic, message.encode('utf-8'))
#    p.flush()
# mytext = "este es un texto en una variable"
# st.text(mytext)
# st.text('this is text')
# st.write('this is the write section')
# "What about this string? Just magic, its like .write?"
# st.divider()
# st.code("val a = 'This is the  code Section, divided with .divider() functino.  where you can scape using \\ character'")
# st.caption('This is caption, to write small text')
# generating the Kafka Consumer
my_consumer = KafkaConsumer(
    'output',
     bootstrap_servers = ['workernode1:9092'],
     auto_offset_reset = 'latest',
     enable_auto_commit = False,
     # group_id = 'my-group',
     # value_deserializer = lambda x : loads(x.decode('utf-8'))
     )
# a = my_consumer(0)
# st.text(a)
# lista = ["1","2","3"]
# for i in lista:
# 	st.text(i)
# mensajes = []
st.text("resultados para '" + articulo + "'")
for message in my_consumer:
	mensaje = message.value.decode('utf-8').strip("'")
	st.text((mensaje))
	# mensajes.append(mensaje)
# st.text("un testo")
# st.text(my_consumer.poll())