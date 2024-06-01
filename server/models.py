from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Define a naming convention for the metadata
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize the SQLAlchemy instance with the metadata
db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    __serialize_rules__ = ('-reviews.customer', '-items.customers',)

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    # Define the relationship to reviews
    reviews = relationship('Review', back_populates='customer')
    # Define the association proxy to items through reviews
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    __serialize_rules__ = ('-reviews.item', '-customers.items',)

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    
    # Define the relationship to reviews
    reviews = relationship('Review', back_populates='item')
    # Define the association proxy to customers through reviews
    customers = association_proxy('reviews', 'customer')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    __serialize_rules__ = ('-customer.reviews', '-item.reviews',)

    id = Column(Integer, primary_key=True)
    comment = Column(String)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    item_id = Column(Integer, ForeignKey('items.id'))

    # Define the relationship to Customer
    customer = relationship('Customer', back_populates='reviews')
    # Define the relationship to Item
    item = relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}>'
