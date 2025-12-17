# BoxGames Connect Flask Application

This is a Flask-based web application for BoxGames Connect with the following features:

- User registration and login (with secure password hashing using bcrypt).
- Role-based dashboards for players, owners, and admins.
- Owners can manage venues, grounds, and slots.
- Players can browse venues, filter slots, and book them.
- Admins can manage users and venues.
- Simple search and date filtering for players.
- Responsive UI with sidebars and basic CSS.

## Folder Structure

boxgames/
│
├── app/
│ ├── init.py
│ ├── models.py
│ ├── auth/
│ │ └── routes.py
│ ├── player/
│ │ └── routes.py
│ ├── owner/
│ │ └── routes.py
│ └── admin/
│ └── routes.py
│
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── player/
│ ├── owner/
│ └── admin/
│
├── static/
│ ├── css/
│ │ └── style.css
│ └── js/
│ └── validation.js
│
├── run.py
└── README.md