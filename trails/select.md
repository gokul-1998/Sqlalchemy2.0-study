```
session.execute(
    select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
).all()
```