from json import dumps

from kafka import KafkaProducer
from kafka import KafkaConsumer
#pip install kafka-python


import streamlit as st


st.title('Bienvenido a ElMercado.com')
st.header('Estás en la seccion de busqueda')
st.subheader('Busca aqui el artículo que quieras comprar')
articulo= st.text_input("Describe tu articulo")
# tienda = st.text_input("Quieres comprar en una tienda en particular? Introduce el nombre de la tienda")
# initializing the Kafka producer
my_producer = KafkaProducer(
    bootstrap_servers = ['workernode1:9092'],
    value_serializer = lambda x:dumps(x).encode('utf-8')
    )
def sendMessage ():
    my_producer.send('streaming-query', value = articulo)

buy = st.button('BUSCAR', 'key1', 'this button is used to buy stuff', on_click=sendMessage)

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

st.text("resultados para '" + articulo + "'")
for message in my_consumer:
	mensaje = message.value.decode('utf-8').strip("'")
	st.text((mensaje))
	# mensajes.append(mensaje)
# st.text("un testo")
# st.text(my_consumer.poll())