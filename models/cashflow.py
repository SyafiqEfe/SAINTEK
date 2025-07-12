from extensions import db
from datetime import datetime

class CashFlow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<CashFlow {self.type} {self.amount}>'
