"""Mock data for LOCSAM UI demo (no MySQL)."""

LOCATIONS = [
    {
        "id": 1,
        "name": "Registan Square",
        "category": "Monument",
        "city": "Samarkand, Uzbekistan",
        "description": (
            "Registan Square is the heart of Samarkand and one of the most magnificent "
            "squares in the world. It is surrounded by three majestic madrasahs built "
            "during the Timurid era and represents the cultural and architectural "
            "heritage of Uzbekistan."
        ),
        "rating": 4.8,
        "reviews": 230,
        "price": 10,
        "open_time": "06:00 AM - 09:00 PM",
        "latitude": 39.6542,
        "longitude": 66.9747,
        "image": "registan",
    },
    {
        "id": 2,
        "name": "Shah-i-Zinda",
        "category": "Monument",
        "city": "Samarkand, Uzbekistan",
        "description": (
            "A famous necropolis containing beautifully decorated mausoleums and "
            "sacred Islamic architecture."
        ),
        "rating": 4.7,
        "reviews": 180,
        "price": 5,
        "open_time": "06:00 AM - 09:00 PM",
        "latitude": 39.6622,
        "longitude": 66.9797,
        "image": "shah_i_zinda",
    },
    {
        "id": 3,
        "name": "Bibi-Khanym Mosque",
        "category": "Mosque",
        "city": "Samarkand, Uzbekistan",
        "description": (
            "One of the largest and most impressive mosques in Central Asia built by "
            "Amir Timur."
        ),
        "rating": 4.6,
        "reviews": 150,
        "price": 5,
        "open_time": "06:00 AM - 09:00 PM",
        "latitude": 39.6605,
        "longitude": 66.9790,
        "image": "bibi_khanym",
    },
    {
        "id": 4,
        "name": "Amir Temur Mausoleum",
        "category": "Monument",
        "city": "Samarkand, Uzbekistan",
        "description": (
            "The final resting place of Amir Timur and an important historical monument."
        ),
        "rating": 4.9,
        "reviews": 210,
        "price": 8,
        "open_time": "06:00 AM - 09:00 PM",
        "latitude": 39.6486,
        "longitude": 66.9697,
        "image": "amir_temur",
    },
    {
        "id": 5,
        "name": "Ulughbek Observatory",
        "category": "Museum",
        "city": "Samarkand, Uzbekistan",
        "description": (
            "An observatory established by Ulughbek that contributed significantly "
            "to astronomy."
        ),
        "rating": 4.5,
        "reviews": 120,
        "price": 5,
        "open_time": "06:00 AM - 09:00 PM",
        "latitude": 39.6747,
        "longitude": 66.9967,
        "image": "ulughbek",
    },
    {
        "id": 6,
        "name": "Tillya-Kori Madrasah",
        "category": "Museum",
        "city": "Samarkand, Uzbekistan",
        "description": (
            "Known for its stunning golden interior and educational significance."
        ),
        "rating": 4.7,
        "reviews": 170,
        "price": 6,
        "open_time": "06:00 AM - 09:00 PM",
        "latitude": 39.6545,
        "longitude": 66.9750,
        "image": "tillya_kori",
    },
]

TICKET_TYPES = [
    {"type": "Adult Ticket", "price": 10, "note": "Age: 16+ years"},
    {"type": "Student Ticket", "price": 5, "note": "Requires Student ID"},
    {"type": "Children Ticket", "price": 3, "note": "Age: 7-12 years"},
    {"type": "Family Ticket", "price": 25, "note": "2 adults + 2 children"},
]

SAMPLE_TICKETS_UPCOMING = [
    {
        "location": "Registan Square",
        "date": "25 May",
        "time": "10:00 AM",
        "detail": "1 Adult",
        "price": 10,
        "status": "upcoming",
    },
    {
        "location": "Shah-i-Zinda",
        "date": "28 May",
        "time": "11:00 AM",
        "detail": "1 Adult",
        "price": 5,
        "status": "upcoming",
    },
    {
        "location": "Ulughbek Observatory",
        "date": "30 May",
        "time": "09:00 AM",
        "detail": "1 Adult",
        "price": 5,
        "status": "upcoming",
    },
]

FILTER_TABS = ["All", "Popular", "Museum", "Mosque", "Monument"]
