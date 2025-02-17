from os import path
from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user


db = SQLAlchemy()
babel = Babel()
migrate = Migrate()
bcrypt = Bcrypt()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['FLASK_ENV'] = 'development'
    app.config['SECRET_KEY'] = 'anykd2424fdf1'
    app.config['SESSION_COOKIE_SECURE'] = True  
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(path.dirname(__file__), DB_NAME)}'

    db.init_app(app)
    babel.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login' 
    

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    with app.app_context():
        create_database(app)
    
    from .models import Tovar, Order, Point, User
    from website.admin.admin_views import MyMainView

    from website.admin.user_view import UserView
    from website.admin.tovar_view import TovarView
    from website.admin.order_view import OrderView
    from website.admin.point_view import PointView
    from website.admin.image_view import ImageView
    from website.admin.video_view import VideoView

    admin = Admin(app, 'Logout', index_view=MyMainView(), template_mode='bootstrap4', url='/logout')

    admin.add_view(UserView(User, db.session))
    admin.add_view(TovarView(Tovar, db.session))
    admin.add_view(OrderView(Order, db.session))
    admin.add_view(PointView(Point, db.session))
    admin.add_view(ImageView())  
    admin.add_view(VideoView()) 

    return app

def create_database(app):
    if not path.exists(f'website/{DB_NAME}'):
        with app.app_context():
            db.create_all()
        print('Created Database!')
        from .models import Tovar, Point, User
        if User.query.count() == 0:
            User_data = [
                ('shin', '1234', True)
            ]
        for data in User_data:
            user = User(
                username=data[0],
                password_hash = data[1],
                is_admin = data[2]
            )
            db.session.add(user)

        if Tovar.query.count() == 0:
            Tovar_data = [
                ('Tokyo Ghoul', 'Mat', 0, 29.99, 'Soon', 'Anime', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 'Tokyo_Ghoul'), 
                ('Samurai red', 'Mat', 65, 29.99, 'In stoke', 'Pixel art', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'A samurai has no purpose, only a path... This mat will fit perfectly and decorate the setup! Colorful art is suitable for absolutely everyone, from novice game lovers to top esports players from different parts of the gaming world!', 'Samurai_red'),
                ('Samurai Large', 'Mat', 24, 39.99, 'In stoke', 'Pixel art', '900x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'A samurai has no purpose, only a path... This mat will fit perfectly and decorate the setup! Colorful art is suitable for absolutely everyone, from novice game lovers to top esports players from different parts of the gaming world!', 'Samurai_Large'),      
                ('Pixel Art Mirage', 'Mat', 44, 29.99, 'In stoke', 'Pixel art', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 'Pixel_Art_Mirage'),
                ('Pixel Art Inferno', 'Mat', 52, 29.99, 'In stoke', 'Pixel art', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 'Pixel_Art_Inferno'),  
                ('Samurai', 'Mat', 24, 29.99, 'In stoke', 'Pixel art', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'A samurai has no purpose, only a path... This mat will fit perfectly and decorate the setup! Colorful art is suitable for absolutely everyone, from novice game lovers to top esports players from different parts of the gaming world!', 'Samurai'),
                ('Pixel Art Dust II', 'Mat',  14, 29.99, 'In stoke', 'Pixel art', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 'Pixel_Art_Dust_II'),    
                ('Black A1', 'Mat', 4, 29.99, 'In stoke', 'Black', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 'Black_A1'),    
                ('Mixed Angularity', 'Mat',  0, 29.99, 'Sold', 'Black', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 'Mixed_Angularity'),    
            ]
            for data in Tovar_data:
                tovar = Tovar(
                    name=data[0],
                    type = data[1],
                    count=data[2],
                    cost = data[3],
                    status = data[4],
                    color = data[5],
                    size = data[6],
                    thickness = data[7],
                    material = data[8],
                    base = data[9],
                    info = data[10],
                    img_name = data[11]
                )
                db.session.add(tovar)

            Tovar_data2 = [
                ('BACKPACK', 
                 'Clothes', 
                 40, 
                 49.99, 
                 'In stoke', 
                 'Black',
                '28.5 sm', 
                '50 sm', 
                '14 sm', 
                'Cordura 1000D, 100% nylon', 
                'Oxford 210D, 100% polyester',
                'three-layer mesh, sealed with foam plastic', 
                'spiral water-repellent', 
                'plastic', 
                'Backpack', 
                'The perfect companion for your daily life! The elegant lines and minimalist style make this backpack a great addition to any look. The backpack is made of high-quality materials, ensuring a long service life. Combine style and practicality in one product')
            ]
            for data in Tovar_data2:
                tovar2 = Tovar(
                    name=data[0],
                    type = data[1],
                    count=data[2],
                    cost = data[3],
                    status = data[4],
                    color = data[5],

                    height = data[6],
                    width = data[7],
                    depth = data[8],
                    upper_material = data[9],
                    ining_material = data[10],
                    back_straps = data[11],
                    zipper = data[12],
                    fastexes_buckles = data[13],
                    img_name = data[14],
                    info = data[15]
                )
                db.session.add(tovar2)

        if Point.query.count() == 0:
            point_data = [
            ('Minsk', 'ul. Installers, 2 Euroopt', 1),
            ('Minsk', 'ul. Prytytsky , 29 1st floor of the Tikali shopping center', 6),
            ('Minsk', 'ul. Kazimirovskaya, 6 m-n Euroopt', 9),
            ('Gomel', 'ul. Kirova, 136 m-n Euroopt', 10),
            ('Vitebsk', 'ave. Builders, 15-2 m-n "Euroopt"', 11),
            ('Lida', 'ul. Krasnoarmeyskaya, 63 m-n Euroopt', 23),
            ('Bobruisk', 'ul. Minskaya, 111 m-n "Euroopt"', 27),
            ('Smorgon', 'ul. Kolasa, 120a m-n "Euroopt"', 29),
            ('Osipovichi', 'ul. Leninskaya, 86B m-n "Kopeechka"', 33),
            ('Glubokoe', 'ul. Lenin, 9A-1 m-n "Euroopt"', 35),
            ('Grodno', 'ul. Solomova, 104/1 m-n "Euroopt"', 37),
            ('Lida', 'ul. Gagarina, 27 m-n "Euroopt"', 38),
            ('Slonim', 'Yershova str., 58 m-n "Euroopt"', 41),
            ('Minsk', 'ul. Bogdanovich, 134 m-n "Hit"', 50),
            ('Svisloch', 'ul. Tsagelnik, 12 m-n "Euroopt"', 51),
            ('Mstislavl', 'Peter Mstislavets str., 1 m-n Euroopt', 53),
            ('Zhlobin', 'mkr. 18th, 43 m-n "Kopek"', 54),
            ('Novogrudok', 'ul. Sovetskaya, 17 m-n "Euroopt"', 57),
            ('Zhodino', 'Gagarin str., 20A', 59),
            ('Dzerzhinsk', 'Minskaya str., 27', 60),
            ('Rogachev', 'Bogatyreva str., 118 m-n "Euroopt"', 61),
            ('Mogilev', '79 Gagarin str., m-n "Euroopt"', 62),
            ('Grodno', ' ave. Kupala, 82A m-n "Euroopt"', 63),
            ('Vitebsk', 'ave. Moskovsky, 130 m-n "Euroopt"', 64),
            ('Brest', 'Varshavskoe highway, 11 m-n "Euroopt"', 65),
            ('Minsk', ' ave. Pushkin, 29b m-n "Groshyk"', 69),
            ('Minsk', ' ave. Pobediteley, 89 m-n "Euroopt"', 74),
            ('Soligorsk', 'Zheleznodorozhnaya str., 12a m-n "Euroopt"', 77),
            ('Ivatsevichi', 'ul. Sovetskaya, 1A', 80),
            ('Narovlya', 'Korzun A.G. str., 64', 83),
            ('Branch', 'Zaslonov str.', 84),
            ('Chechersk', ' lane Pervomaisky, 4', 85),
            ('Bridges', ' ave. Mira, 2a', 88),
            ('Gomel', ' Khataevich str., 9', 89),
            ('Minsk', 'Umanskaya str., 54 Globo shopping center near the parking lot', 92),
            ('Baranovichi', 'ul. Textile, 14a m-n "Euroopt"', 93),
            ('Klichev', 'Zaytsa str., 4a m-n "Euroopt"', 94),
            ('Minsk', 'ave. Rokossovsky, 99', 96),
            ('Minsk', 'Yesenin str., 76', 100),
            ('Minsk', 'Masherov Ave., 51', 107),
            ('Minsk', 'ul. Kazinets, 52a', 108),
            ('Mogilev',  '40A Movchanskogo str.', 112),
            ('Petrikov', '3B Paper street', 115),
            ('Shumilino', 'Leninskaya Street, 32 m-n "Euroopt"', 119),
            ('Vitebsk', ' ave. Moskovsky, 60a', 121),
            ('Minsk', ' 44 Yankovsky str.', 123),
            ('Minsk', ' Alibegova str., 13/1', 125),
            ('Brest', ' ul. 17 September, 49', 126),
            ('Vitebsk', ' Lenin str., 26a', 127),
            ('Brest', 'Raduzhnaya str., 150', 128),
            ('Lelchitsy', ' ul. Sovetskaya, 28', 130),
            ('Vileika', 'Chapaev str., 60', 131),
            ('Mozyr', 'ul. Studentskaya, 46', 132),
            ('Brest', 'St. Orlovskaya, 50', 136),
            ('Minsk', 'Matusevich str., 35G', 137),
            ('Khoiniki', '70 let Oktyabrya str., 1', 138),
            ('Chashniki', 'ul. Cosmonauts, 4', 139),
            ('Khotimsk', 'ul. Leninskaya, 1', 140),
            ('Braslav', 'Dzerzhinsky str., 28B', 141),
            ('Minsk', 'Goshkevich str., 3', 142),
            ('Molodechno', 'ul. Budavnikov, 17A', 146),
            ('Glusk', 'ul. Gagarina, 25', 147),
            ('Minsk', 'ul. Shpilevsky, 54', 148),
            ('Grodno', 'ul. Oginsky, 12', 151),
            ('Brest', 'Moskovskaya str., 342', 152),
            ('Minsk', 'ya.Kolas str., 53/1', 158),
            ('Minsk', 'Lyubimova Ave., 26', 159),
            ('Minsk', 'Aerodromnaya str., 28', 160),
            ('Minsk', 'ul. Vodolazhsky, 15', 161),
            ('Minsk', 'Burdeynogo str., 6B (shopping center "TOP")', 165),
            ('Minsk', 'ul. Karvata, 31a', 167),
            ('Baranovichi', 'ul. Communist, 5', 168),
            ('Mogilev', 'ul. Chestnut, 4', 175),
            ('Mozyr', 'b-R. Friendship, 3a', 176),
            ('Novopolotsk', 'ul. Yeronko, 7a', 178),
            ('Rechitsa', 'ul. Dostoevsky, 27-54', 180),
            ('Minsk', 'ul. Prushinsky, 2', 182),
            ('Minsk', 'ul. Bagration, 55b', 183),
            ('Pinsk', 'ul. Brest, 72a', 186),
            ('Kopyl', 'ul. Partizanskaya, 1a', 187),
            ('Gomel', 'ave. Rechitsky, 5B', 190),
            ('Gorki', 'ul. Sovetskaya, 9', 192),
            ('Gomel', 'ul. Kirova, 25', 193),
            ('Minsk', 'ave. Partizansky, 13', 194),
            ('Gantsevichi', 'ul. Builders, 11B', 200),
            ('Gomel', 'ul. Tsarikova, 1/2', 203),
            ('Minsk', 'ave. Dzerzhinsky, 23-431', 206),
            ('Vitebsk', 'ave. Frunze, 37', 208),
            ('Minsk', 'tr-T. Smorgovsky, 7-93', 211),
            ('Ivanovo', 'ul. Sovetskaya, 55', 216),
            ('Kamenets', 'ul. Borderline, 22', 217),
            ('Verkhnedvinsk', 'ul. Leninskaya, 15b-1', 218),
            ('Baranovichi', 'ave. Sovetsky, 35', 219), 
            ('Gomel', '62A Rechitsky Ave.', 220),
            ('Orsha', 'ul. Mira, 49', 221),
            ('Buda-Koshelevo', 'ul. Lenin, 58', 223),
            ('Round', 'street Moprovskaya, 6 (m-n "Euroopt")', 224),
            ('Minsk', 'ul. Jerzy Gedroica, 2', 226),
            ('Zhitkovichi', 'ul. Chkalova, 6', 228),
            ('Ivye', 'Karl Marx Street, 19', 232),
            ('Berezino', 'ul. Honinova, 29b1', 236),
            ('Soligorsk', 'ul. Embankment, 25A', 239),
            ('Cherven', 'ul. Leninskaya, 5', 242),
            ('Minsk', 'ul. Lobanka, 22', 244),
            ('Kolodishchi', 'ul. Minsk, 69A', 246),
            ('Yelsk', 'Dzerzhinskiy str., 20-2', 249),
            ('Bykhov', 'ul. Bogdan Khmelnitsky, 1', 250),
            ('Slutsk', 'ul.Socialist, 144a', 251),
            ('Druzhny', 'ul.Chepika, 26', 253),
            ('Fanipol', 'ul. Chapsky, 15', 256),
            ('Miory', 'str. Sadovaya, 1', 260),
            ('Drogichin', 'ul. Reclamation, 43/1', 262),
            ('Berezovka', 'ul. Komsomolskaya 22', 263),
            ('Grodno', 'ul. Soviet Border Guards, 91', 264),
            ('Grodno', 'str. Dovator, 7', 265),
            ('Orsha', 'Alexey Garanin Ave., 4', 267),
            ('Minsk', 'ul.Mogilevskaya, 14', 269),
            ('Borisov', 'ul. Normandy-Neman, 145', 276),
            ('Bobruisk', 'ul. Sovetskaya, 113', 279),
            ('Mogilev', 'ul. Pervomaiskaya, 69A', 282),
            ('Lyuban', 'ul. Sovetskaya, 31', 284),
            ('Minsk', 'ave. Dzerzhinsky, 104k2, room117, entrance through the business center', 285),
            ('Beloozersk', 'ul. Lenin, 50A', 286),
            ('Logoisk', 'Gainenskoe highway, 1-117', 287),
            ('Luninets', 'ul. Sovetskaya, 13-3', 289),
            ('Grodno', 'Kurchatov str., 47', 292),
            ('Minsk', 'ul.Lozhinskaya, 20', 294),
            ('Kalinkovichi', 'ul. 50 let Oktyabrya, 83', 295),
            ('Oshmyany', 'ul. Pionerskaya, 2', 299),
            ('Minsk', 'ul.Tashkent, 10', 300),
            ('Brest', 'St.Rokossovsky, 3-85', 302),
            ('Minsk', 'ave. Dzerzhinsky, 11', 303),
            ('Novopolotsk', 'Molodezhnaya str., 51-63', 305),
            ('Minsk', 'ul.Kamennogorskaya, 6-203', 311),
            ('Mogilev', 'ul. Arkady Kuleshova, 1', 312),
            ('Minsk', 'ul. Kulman, 5B-72, Pavilion No.135', 314),
            ('Mogilev', 'ave. Pushkinskiy, 30 (m-n "Euroopt")', 318),
            ('Skidel', 'ul. Gagarina, 11', 319),
            ('Lida', 'ul. Sovetskaya, 41-3', 320),
            ('Bobruisk', 'ul. Batova, 19-A', 322),
            ('Slutsk', 'Levonyan str., 31A', 324),
            ('Cherikov', 'ul. Leninskaya Street, 178', 325),
            ('Zhabinka', 'ul. Naganova, 16a/2', 326),
            ('Minsk', 'ul. Akademika Zhebraka, 35', 327),
            ('Smolevichi', '50 let Oktyabrya str., 4-2', 328),
            ('Mogilev', 'ul. Lazarenko, 73a', 329),
            ('Minsk', 'Surganova str., 57b-8', 331),
            ('Brest', 'St. Komsomolskaya, 8-1 (m-n "Euroopt")', 333),
            ('Brest', 'Lutskaya str., 48', 334),
            ('Pinsk', 'ul. Karaseva, 6', 335),
            ('Kobrin', 'Dzerzhinskiy str., 115b', 336),
            ('Grodno', 'ul. Antonova, 14-43', 337),
            ('Luninets', 'ul. Krasnaya, 107-2', 339),
            ('Ostrovets', 'Karl Marx Street, 1', 340),
            ('Polotsk', 'ul. Petrusya Brovki, 45-2', 341),
            ('Vitebsk', 'ul. Chkalova, 56-154', 342),
            ('Nesvizh', 'ul. Leninskaya, 115', 343),
            ('Vitebsk', '3rd Zmitroka Byaduli str., 28-2', 346),
            ('Brest', 'ave. Masherova, 59-41', 347),
            ('Polotsk', 'Pushkin str., 20-1', 351),
            ('Kalinkovichi', 'ul.Sovetskaya, 96-1', 352),
            ('Minsk', 'ul. Angarsk, 62a', 354),
            ('Dyatlovo', 'ul. Gorky, 12', 357),
            ('Lepel', 'Chuikov str., 75', 358),
            ('Chausy', 'Azarov str., 2A', 359),
            ('Slutsk', 'ul. Lenin, 187-1', 361),
            ('Minsk', ' Belinsky str., 54-275', 364),
            ('Minsk', 'Bogdanovicha str., 89-2H', 369),
            ('Shklov', 'Fabrichnaya str., 26A', 371),
            ('Borisov', ' Chapaev str., 27-43', 372),
            ('Gomel', 'Sukhoi str., 1B', 374),
            ('Pruzhany', ' lane. Aptekarsky, 4B', 376),
            ('Molodechno', 'ul. Volynets, 9-23', 377),
            ('Rogachev', 'Lenin str., 41-15', 380),
            ('Minsk', 'Rotmistrova str., 42', 382),
            ('Novopolotsk', 'Molodezhnaya str., 134-178', 384),
            ('Minsk', 'Romanovskaya Sloboda str., 13-5H', 385),
            ('Rechitsa', 'Grigory Shirma str., 30', 389),
            ('Brest', 'Volgogradskaya str., 4A-1', 390),
            ('Volkovysk', 'Lenin str., 57', 392),
            ('Gomel', 'ave. October, 2B', 393),
            ('Uzda', 'K.Marx Street, 90/2', 396),
            ('Minsk', 'Nikola Tesla Street, 6-1', 398),
            ('Pinsk', ' ave. Zholtovsky, 10-34', 399),
            ('Minsk', 'Nalibokskaya str., 12', 401),
            ('Gomel', 'Ilyich str., 333', 402),
            ('Bobruisk', 'Baharova str., 31', 405),
            ('Krichev', ' mkr. Sozh, 11', 406),
            ('Myadel', 'N.K. Krupskaya str., 5', 408),
            ('Borisov', 'Trusova str., 32-2', 412),
            ('Mozyr', 'b-R. Youth, 59A. Boulevard shopping Center', 413),
            ('Columns', 'Leninskaya str., 91', 415),
            ('Brest', 'Makhnovich str., 35-88', 416),
            ('Lyakhovichi', 'September 17 str., 7', 419),
            ('Baranovichi', 'ul. Voikova, 14-13', 420),
            ('Klimovichi', 'ul. Sovetskaya, 65A', 421),
            ('Grodno', 'Viktor Sayapin str., 10-84', 422),
            ('Maryina Gorka', 'Leninskaya str., 63-3', 433),
            ('Dokshitsy', 'Pionerskaya str., 18-2', 437),
            ('Shchuchin', 'ul. Lenin, 36-4', 439),
            ('Svetlogorsk', 'Sportivnaya str., 11/1-1', 442),
            (' Minsk', ' Kalinovskiy str., 101', 443),
            ('Baranovichi', 'F.Skaryna str., 17A', 444),
            ('Grodno', ' Suvorov str., 298', 445),
            ('Kobrin', 'Pushkin str., 14-89 (m-n "Euroopt)', 448),
            ('Grodno', ' Dzerzhinskiy str., 101-3', 453),
            ('Baran', 'Orshanskaya str., 26a', 454),
            ('Novolukoml', 'Kommunalnaya str., 1', 456),
            ('Dobrush', 'Knyaz Paskevich str., 13-49', 459),
            ('Svetlogorsk', 'Azalova str., in the area of house No. 61', 463),
            ('Stolin', 'Bykovsky str., 29/1', 465),
            ('Gorodok', '87-1 K.Marx Street', 467),
            ('Machulishchi', ' Molodezhnaya str., 39', 469),
            ('Minsk', 'Yesenina str., 30 room 2H', 470),
            ('Soligorsk', 'Molodezhnaya str., 6', 471),
            ('Vitebsk', 'Gorovets str., 8a', 472),
            ('Orsha', ' Vladimir Lenin str., 25-57', 473),
            ('Gomel', 'Sviridov str., 13',474),
            ('Malorita', 'Lermontov str., 4', 478),
            ('Polotsk', 'Shenyagin str., 54', 481),
            ('Lida', ' Varshavskaya str., 58, room 2', 483),
            ('Minsk', ' Oleg Koshevoy str., 8-2', 484),
            ('Soligorsk', ' ul. Oktyabrskaya, 27a',485),
            ('Volozhin', ' pl. Freedom, 5', 487),
            ('Mogilev', 'Gomelskoe sh., 55/1', 488),
            ('Lida', 'Kachana str., 29', 491),
            ('Mozyr', 'Malinina str., 1a', 492),
            ('Minsk', 'Malinina str., 24', 494),
            ('Mogilev', 'Yakubovsky str., 51B', 495),
            ('Tolochin', 'Lenin str., 53a', 496),
            ('Brest', 'Pisatel Smirnov str., 19A-62', 497),
            ('Minsk', 'Varvasheni str., 16-1', 501),
            ('Kletsk', 'Pervomayskaya str., 6', 503),
            ('Vitebsk', ' ave. Builders, 1', 506),
            ('Minsk', ' Knyagininskaya str., 10-66', 507),
            ('Vitebsk', ' Budennogo str., 7', 508),
            ('Gomel', 'Katunina str., 5-46', 510),
            ('Baranovichi', 'Kabushkina str., 108', 512),
            ('Old Roads', 'Sverdlov str., 39', 513),
            ('Minsk', 'Sukharevskaya str., 62', 514),
            ('Minsk', 'Biryuzova str., 11', 515),
            ('Minsk', 'Kamennogorskaya str., 66', 516),
            ('Slutsk', 'Maxim Bogdanovich str., 21', 518),
            ('Minsk', 'Kiselyov str., 17-56', 519),
            ('Kostyukovichi', ' Molodezhny Microdistrict, 13', 520),
            ('Minsk', 'Gamarnik str., 30 room 271', 522),
            ('Postavy', '17 September str., 1-6', 523),
            ('Gomel', '6-1 Vladimirova str.', 524),
            ('Mogilev', 'Grunvaldskaya str., 26-466', 525),
            ('Belynichi', 'Kalinina str., 40', 526),
            ('Krupki', ' Kirova str., 7/1', 527),
            ('Minsk', 'Grekova str., 4-92', 528),
            ('Zaslavl', 'ul. Sovetskaya, 112/1', 531),
            ('Minsk', ' Kolesnikova str., P.R., 20-135', 532),
            ('Grodno', ' 5a Vrublevsky str.', 533),
            ('Birch', 'ul. Oktyabrskaya, 27-3', 534),
            ('Minsk', 'Mikhail Lynkova str. 17-1N', 536),
            ('Minsk', 'MKAD str., 301-1, administrative and commercial premises No. 1-6', 537),
            ('Vitebsk', '1st Proletarskaya str., 10', 538), 
            ('Dzerzhinsk', '4A Sharko str.', 539),
            ('Baranovichi', '50-5 Komsomolskaya str.', 540),
            ('Minsk district', ' Senitsky village, 84, district d. Senica-Kopievichi', 542),
            ('Gomel', '93B Sviridova str.', 545),
            ('Minsk', '40 Plekhanov str., room 1H', 546),
            ('Radoshkovichi', 'ul. Proletarskaya, 2A', 547),
            ('Minsk', 'Franziska Skaryna str., 5-438', 548),
            ('Borovlyany', 'Birch Grove str., 108-47', 549),
            ('Birch', 'Komsomolskaya, 3B-1', 550),
            ('Galevo', ' Pervomaiskaya str., 176A/2 (Pinsk)', 551),
            ('Grodno', '91 Maxim Gorky str. (Korona market, hall D-13).', 552),
            ('Zhlobin', 'Petrovsky str., 27A', 553),
            ('Minsk', 'ave. Independence, 168/1-3H', 554),
            ('Minsk', ' Narodnaya str., 31-1N', 556),
            ('Zhodino', 'ave. Lenin, 21/2-8j', 557),
            ('Mikashevichi', 'Pervomaiskaya str., 14-37', 558),
            ('Grodno', 'Shchors str., 11B-3', 666),
            ('Grodno', 'Kupala str., 87 (Trinity Shopping Center, 3 floor)', 777),
            ('Pinsk', ' 32 K. Marx street', 888),
            ]
            for data in point_data:
                point = Point(
                    city=data[0],
                    street=data[1],
                    number = data[2]
                )
                db.session.add(point)
        db.session.commit()

