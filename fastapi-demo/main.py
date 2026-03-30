from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from model import product as ProductSchema
import databasemodel
from database import Session as SessionLocal, engine

app = FastAPI()

databasemodel.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    
    return {"message": "Hello World"}

products = [
    ProductSchema(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    ProductSchema(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    ProductSchema(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    ProductSchema(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def init_db():
    db = SessionLocal()
    try:
        count = db.query(databasemodel.product).count()
        if count == 0:
            for product in products:
                db.add(databasemodel.product(**product.model_dump()))
            db.commit()
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/products", response_model=list[ProductSchema])
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(databasemodel.product).all()
    return [ProductSchema.model_validate(item, from_attributes=True) for item in db_products]

@app.get("/product/{id}", response_model=ProductSchema)
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    raise HTTPException(status_code=404, detail="product not found")


@app.post("/product", response_model=ProductSchema,)
def add_product(product: ProductSchema):
    products.append(product)
    return product


@app.put("/product")
def update_product(id: int, product: ProductSchema):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "product updated successfully"
    raise HTTPException(status_code=404, detail="no product found")


@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product deleted successfully"
    raise HTTPException(status_code=404, detail="no product found")

