from tables import User, Reagent, Supplier, Product, Reagent, Grid, InTag, OutTag, Session

import pymysql
from sqlalchemy import exc

# --------------------------

s = Session()

_objects = s.query(InTag).order_by(InTag.stockIn_alpha.asc()).all()

print("In, Alpha: ", _objects)

s.close()
