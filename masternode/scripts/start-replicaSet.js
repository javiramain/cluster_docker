rs.initiate()
rs.add("workernode1:27017")
rs.add("workernode2:27017")
rs.add("workernode3:27017")
cfg=rs.conf()
cfg.members[0].priority=2
cfg.members[1].priority=1
cfg.members[2].priority=1
cfg.members[3].priority=1
rs.reconfig(cfg)
var variosArticulos=[{"id_articulo":"0001", "nombre_articulo":"iphone 11 128Gb", "palabras_clave":["iphone","11","128gb","iphone11"],"caracteristicas_venta":{"marca":"Apple","precio":999,"almacenamiento":"128Gb","memoria":"4 Gb", "tamano":"6 pulgadas","conector":"lightning"}},{"id_articulo":"0002", "nombre_articulo":"conga 4690", "palabras_clave":["conga","conga 4690","4690","aspiradora", "robot limpieza", "robot aspirador","robot"],"caracteristicas_venta":{"marca":"Cecotec","precio":200,"potencia succion":"alta","autonomia":"8 horas","peso":"3 kilogramos","conector":"lightning"}}]
use elmercado
db.articulos
db.articulos.insert(variosArticulos)