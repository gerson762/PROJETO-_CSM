CREATE TABLE User (
    id Int PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCAHR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    id int PRIMARY KEY AUTO_INCREMENT,
    courses_name VARCHAR(255) NOT NULL,
);

CREATE TABLE testimonials (
    id int PRIMARY KEY AUTO_INCREMENT,
    User_id int,
    testimonials_text TEXT NOT NULL,
    foreign KEY (usser_id) references users(id)
);

insert into courses (course_name) values 
('GESTÃO DE PROJETOS'),
('PROGRAMAÇÃO EM PYTHON'),
('MARKETING DIGITAL'),
('DESING GRAFICO');

insert into users (email, password_hash, full_name) values
('teste@educaprime.com', 'hash_da_senha_segura', 'usuário de teste');