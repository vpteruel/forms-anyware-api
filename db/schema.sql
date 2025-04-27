create database hpha;
use hpha;

-- Purpose: Create a table to store the users.
create table users (
    id bigint unsigned auto_increment primary key,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    username varchar(255),
    email varchar(255) not null,
    password varchar(255) not null,
    is_admin tinyint(1) not null default 0,
    last_login timestamp,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp
);

alter table users
add unique index unique_user_email (email);

-- Purpose: Create a table to store the departments.
create table departments (
    id bigint unsigned auto_increment primary key,
    name varchar(255) not null,
    code varchar(255) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp
);

alter table departments
add unique index unique_department (name, code);

-- Purpose: Create a table to store the roles.
create table roles (
    id bigint unsigned primary key,
    name varchar(255) not null
);

alter table roles
add unique index unique_role_name (name);

insert into roles (id, name) values
    (1, 'Administrator'),
    (2, 'Initiator'),
    (3, 'Delegate'),
    (4, 'Supervisor'),
    (5, 'Manager'),
    (6, 'Director'),
    (7, 'VP for Department'),
    (8, 'VP / CFE'),
    (9, 'CEO'),
    (10, 'Board Chair');

-- Purpose: Create a table to store the users and their roles in the departments.
create table departments_users_roles (
    id bigint unsigned auto_increment primary key,
    department_id bigint unsigned not null,
    user_id bigint unsigned not null,
    role_id bigint unsigned not null,
    foreign key (department_id) references departments(id),
    foreign key (user_id) references users(id),
    foreign key (role_id) references roles(id)
);

alter table departments_users_roles
add unique index unique_department_user_role (department_id, user_id, role_id);

-- Purpose: Create a table to store the sites.
create table sites (
    id bigint unsigned auto_increment primary key,
    name varchar(100) not null,
    mnemonic varchar(20) not null,
    location varchar(60) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp
);

alter table sites
add unique index unique_site (mnemonic);

insert into sites (name, mnemonic, location) values
    ('Stratford General Hospital', 'SGH', 'Stratford'),
    ('Seaforth Community Hospital', 'SEA', 'Seaforth'),
    ('Alexandra & Marine General Hospital', 'AMGH', 'Goderich'),
    ('St. Marys Memorial Hospital', 'SMMH', 'St. Marys'),
    ('Clinton Public Hospital', 'CPH', 'Clinton');

-- Purpose: Create a table to store the PR types.
create table purchase_requisition_types (
    id bigint unsigned auto_increment primary key,
    name varchar(255) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp
);

alter table purchase_requisition_types
add unique index unique_pr_type_name (name);

insert into purchase_requisition_types (name) values
    ('Expense'),
    ('Capital'),
    ('Construction');

-- Purpose: Create a table to store the PR status.
create table purchase_requisition_status (
    id bigint unsigned primary key,
    name varchar(255) not null
);

alter table purchase_requisition_status
add unique index unique_pr_status_name (name);

insert into purchase_requisition_status (id, name) values
    (1, 'Draft'),
    (2, 'Pending'),
    (3, 'Approved'),
    (4, 'Rejected'),
    (5, 'Cancelled');

-- Purpose: Create a table to store the purchase requisitions.
create table purchase_requisitions (
    id bigint unsigned auto_increment primary key,
    site_id bigint unsigned not null,
    type_id bigint unsigned not null,
    department_id bigint unsigned not null,
    user_id bigint unsigned not null,
    status_id bigint unsigned not null,
    pr_number varchar(20) not null,
    po_number varchar(20),
    requisition_date date not null,
    tel_ext varchar(20),
    comments varchar(5000),
    suggested_supplier varchar(200),
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp,
    foreign key (site_id) references sites(id),
    foreign key (type_id) references purchase_requisition_types(id),
    foreign key (department_id) references departments(id),
    foreign key (user_id) references users(id),
    foreign key (status_id) references purchase_requisition_status(id)
);

-- Purpose: Create a table to store the purchase requisition items.
create table purchase_requisition_items (
    id bigint unsigned auto_increment primary key,
    purchase_requisition_id bigint unsigned not null,
    quantity int not null,
    unit_measure varchar(20) not null,
    unit_price decimal(10, 2) not null,
    vendor_catalogue_number varchar(20) not null,
    eoc_cip varchar(20) not null,
    description varchar(5000) not null,
    total decimal(10, 2) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (purchase_requisition_id) references purchase_requisitions(id)
);
