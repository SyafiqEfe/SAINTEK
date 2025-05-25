from extensions import db

class MosqueInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    history = db.Column(db.Text, nullable=True)
    vision = db.Column(db.Text, nullable=True)
    mission = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    logo = db.Column(db.String(255), nullable=True)
    google_maps_link = db.Column(db.String(255), nullable=True)
    
    # Social media links
    facebook = db.Column(db.String(255), nullable=True)
    twitter = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    youtube = db.Column(db.String(255), nullable=True)
    
    # Donation information
    bank_account = db.Column(db.String(100), nullable=True)
    bank_name = db.Column(db.String(100), nullable=True)
    qris_image = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<MosqueInfo {self.name}>'

class QuoteOfTheDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_text = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(200), nullable=True)  # Quran, Hadith, Scholar name
    reference = db.Column(db.String(200), nullable=True)  # Surah & verse, book reference
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<QuoteOfTheDay {self.id}>'